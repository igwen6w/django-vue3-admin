# -*- coding: utf-8 -*-

"""
处置工单任务, 将处置结果同步到市中心工单系统
"""

import logging
import time
from typing import Dict, Any, Optional
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from external_platform.utils import get_task_config
from gateway import disposal_order

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_disposal_order(self, disposal_id: int) -> Dict[str, Any]:
    """将work.models.Disposal中的处置结果同步到外部平台工单系统
    
    该任务由用户添加处置结果后触发，主要职责是：
    1. 获取work.models.Disposal记录数据
    2. 将数据转换为外部平台API所需的格式
    3. 通过disposal_order()进行同步
    4. 更新sync_相关字段（sync_task_name, sync_task_id, sync_status, sync_time, sync_response）
    
    Args:
        disposal_id: work.models.Disposal记录的ID
        
    Returns:
        Dict[str, Any]: 任务执行结果，包含以下字段：
            - success: 是否成功
            - task_id: 任务ID
            - disposal_id: 处置记录ID
            - external_id: 工单ID
            - sync_result: 同步结果详情
            - error: 错误信息（如果有）
    """
    task_id = self.request.id
    logger.info(f"开始同步处置工单数据 - 任务ID: {task_id}, 处置记录ID: {disposal_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'task_id': task_id,
        'disposal_id': disposal_id,
        'external_id': None,
        'sync_result': None,
        'error': None
    }
    
    try:
        # 获取work.models.Disposal记录
        from work_order.models import Disposal
        
        try:
            disposal = Disposal.objects.get(id=disposal_id)
        except Disposal.DoesNotExist:
            error_msg = f"Disposal记录不存在: {disposal_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 检查是否已经同步过
        if disposal.sync_status:
            logger.info(f"处置记录已同步过 - 记录ID: {disposal_id}, 任务ID: {disposal.sync_task_id}")
            result['success'] = True
            result['external_id'] = disposal.external_id
            result['sync_result'] = {'message': '记录已同步，跳过处理'}
            return result
        
        # 准备同步数据
        external_id = disposal.external_id
        if not external_id:
            error_msg = f"Disposal记录缺少external_id: {disposal_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        result['external_id'] = external_id
        
        # 构建disposal_order API所需的参数
        sync_params = _build_disposal_order_params(disposal)
        
        logger.info(f"准备同步处置工单 - external_id: {external_id}, 工单编号: {sync_params.get('record_number')}")
        logger.debug(f"同步参数: {sync_params}")
        
        # 执行同步操作
        try:
            sync_response = disposal_order(sync_params)
            
            if sync_response.get('success', False):
                # 同步成功，更新处置记录状态
                with transaction.atomic():
                    disposal.sync_task_name = 'sync_disposal_order'
                    disposal.sync_task_id = task_id
                    disposal.sync_status = True
                    disposal.sync_time = timezone.now()
                    disposal.sync_response = sync_response
                    disposal.save(update_fields=['sync_task_name', 'sync_task_id', 'sync_status', 'sync_time', 'update_time', 'sync_response'])
                
                result['success'] = True
                result['sync_result'] = sync_response
                
                execution_time = int((time.time() - start_time) * 1000)
                logger.info(f"处置工单同步成功 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                           f"external_id: {external_id}, 耗时: {execution_time}ms")
                
            else:
                # 同步失败
                error_msg = f"外部API调用失败: {sync_response.get('error', '未知错误')}"
                logger.error(f"处置工单同步失败 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                            f"external_id: {external_id}, 错误: {error_msg}")
                
                result['error'] = error_msg
                result['sync_result'] = sync_response
                
                # 将错误信息记录到处置记录中（可选）
                # disposal.sync_task_id = task_id
                # disposal.save(update_fields=['sync_task_id', 'update_time'])
                
        except Exception as api_error:
            error_msg = f"API调用异常: {str(api_error)}"
            logger.error(f"处置工单API调用异常 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                        f"external_id: {external_id}, 异常: {error_msg}", exc_info=True)
            result['error'] = error_msg
            raise api_error
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"同步处置工单异常: {str(e)}"
        logger.error(f"同步处置工单异常 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('sync_disposal_order').get('retry_delay', 60)
            logger.info(f"同步处置工单重试 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                       f"重试次数: {self.request.retries + 1}, 延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result


def _build_disposal_order_params(disposal) -> Dict[str, Any]:
    """构建disposal_order API所需的参数
    
    Args:
        disposal: Disposal实例
        
    Returns:
        Dict[str, Any]: API参数字典
    """
    # 基于gateway/api_wrappers.py中disposal_order方法的参数要求构建
    params = {
        'record_number': disposal.external_record_number,
        'note1': disposal.external_note1,
        'distribute_way': disposal.external_distribute_way,
        'note8': disposal.external_note8,
        'd_attachments': disposal.external_d_attachments,
        'note3': disposal.external_note3,
        'note4': disposal.external_note4,
        'note5': disposal.external_note5,
        'note6': disposal.external_note6,
        'note11': disposal.external_note11,
        'note': disposal.external_note,
        'note10': disposal.external_note10,
    }
    
    # 过滤掉None值的参数
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    logger.debug(f"构建disposal_order参数完成 - 工单编号: {disposal.external_record_number}, "
                f"参数数量: {len(filtered_params)}")
    
    return filtered_params


def trigger_sync_disposal_order(disposal_id: int, delay: int = 0) -> Optional[str]:
    """触发处置工单同步任务
    
    Args:
        disposal_id: Disposal记录ID
        delay: 延迟执行秒数，默认立即执行
        
    Returns:
        str: 任务ID，如果触发失败返回None
    """
    try:
        if delay > 0:
            # 延迟执行
            task_result = sync_disposal_order.apply_async(
                args=[disposal_id],
                countdown=delay
            )
        else:
            # 立即执行
            task_result = sync_disposal_order.delay(disposal_id)
        
        task_id = task_result.id
        logger.info(f"处置工单同步任务已触发 - 任务ID: {task_id}, 处置记录ID: {disposal_id}, "
                   f"延迟: {delay}秒")
        
        return task_id
        
    except Exception as e:
        logger.error(f"触发处置工单同步任务失败 - 处置记录ID: {disposal_id}, 错误: {str(e)}", 
                    exc_info=True)
        return None
