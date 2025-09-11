# -*- coding: utf-8 -*-

"""
编辑工单任务, 将编辑后的数据同步到市中心工单系统
"""

import logging
import time
from typing import Dict, Any, Optional
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from external_platform.utils import get_task_config
from gateway.api_wrappers import get_api_instance

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_edit_order(self, edit_record_id: int) -> Dict[str, Any]:
    """将BaseEditRecord中的编辑数据同步到外部平台工单系统
    
    该任务由用户添加编辑记录后触发，主要职责是：
    1. 获取BaseEditRecord记录数据
    2. 将数据转换为外部平台API所需的格式
    3. 通过gateway.api_wrappers.edit_order()进行同步
    4. 更新sync_相关字段（sync_task_id, sync_status, sync_time）
    
    Args:
        edit_record_id: BaseEditRecord记录的ID
        
    Returns:
        Dict[str, Any]: 任务执行结果，包含以下字段：
            - success: 是否成功
            - task_id: 任务ID
            - edit_record_id: 编辑记录ID
            - external_id: 工单ID
            - sync_result: 同步结果详情
            - error: 错误信息（如果有）
    """
    task_id = self.request.id
    logger.info(f"开始同步编辑工单数据 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'task_id': task_id,
        'edit_record_id': edit_record_id,
        'external_id': None,
        'sync_result': None,
        'error': None
    }
    
    try:
        # 获取BaseEditRecord记录
        from work_order.models import BaseEditRecord
        
        try:
            edit_record = BaseEditRecord.objects.get(id=edit_record_id)
        except BaseEditRecord.DoesNotExist:
            error_msg = f"BaseEditRecord记录不存在: {edit_record_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 检查是否已经同步过
        if edit_record.sync_status:
            logger.info(f"编辑记录已同步过 - 记录ID: {edit_record_id}, 任务ID: {edit_record.sync_task_id}")
            result['success'] = True
            result['external_id'] = edit_record.external_id
            result['sync_result'] = {'message': '记录已同步，跳过处理'}
            return result
        
        # 准备同步数据
        external_id = edit_record.external_id
        if not external_id:
            error_msg = f"BaseEditRecord记录缺少external_id: {edit_record_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        result['external_id'] = external_id
        
        # 构建edit_order API所需的参数
        sync_params = _build_edit_order_params(edit_record)
        
        logger.info(f"准备同步编辑工单 - external_id: {external_id}, 工单编号: {sync_params.get('roll_number')}")
        logger.debug(f"同步参数: {sync_params}")
        
        # 执行同步操作
        api = get_api_instance()
        
        try:
            sync_response = api.edit_order(sync_params)
            
            if sync_response.get('success', False):
                # 同步成功，更新编辑记录状态
                with transaction.atomic():
                    edit_record.sync_task_id = task_id
                    edit_record.sync_status = True
                    edit_record.sync_time = timezone.now()
                    edit_record.save(update_fields=['sync_task_id', 'sync_status', 'sync_time', 'update_time'])
                
                result['success'] = True
                result['sync_result'] = sync_response
                
                execution_time = int((time.time() - start_time) * 1000)
                logger.info(f"编辑工单同步成功 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                           f"external_id: {external_id}, 耗时: {execution_time}ms")
                
            else:
                # 同步失败
                error_msg = f"外部API调用失败: {sync_response.get('error', '未知错误')}"
                logger.error(f"编辑工单同步失败 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                            f"external_id: {external_id}, 错误: {error_msg}")
                
                result['error'] = error_msg
                result['sync_result'] = sync_response
                
                # 将错误信息记录到编辑记录中（可选）
                # edit_record.sync_task_id = task_id
                # edit_record.save(update_fields=['sync_task_id', 'update_time'])
                
        except Exception as api_error:
            error_msg = f"API调用异常: {str(api_error)}"
            logger.error(f"编辑工单API调用异常 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                        f"external_id: {external_id}, 异常: {error_msg}", exc_info=True)
            result['error'] = error_msg
            raise api_error
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"同步编辑工单异常: {str(e)}"
        logger.error(f"同步编辑工单异常 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('sync_edit_order').get('retry_delay', 60)
            logger.info(f"同步编辑工单重试 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                       f"重试次数: {self.request.retries + 1}, 延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result


def _build_edit_order_params(edit_record) -> Dict[str, Any]:
    """构建edit_order API所需的参数
    
    Args:
        edit_record: BaseEditRecord实例
        
    Returns:
        Dict[str, Any]: API参数字典
    """
    # 基于gateway/api_wrappers.py中edit_order方法的参数要求构建
    params = {
        'roll_number': edit_record.external_roll_number,
        'payroll_result': edit_record.external_payroll_result,
    }
    
    # 复核相关字段映射
    if edit_record.external_product_ids is not None:
        params['product_ids'] = edit_record.external_product_ids
    
    if edit_record.external_addr2 is not None:
        params['addr2'] = edit_record.external_addr2
    
    if edit_record.external_company_address is not None:
        params['company_address'] = edit_record.external_company_address
    
    if edit_record.external_order_number is not None:
        params['order_number'] = edit_record.external_order_number
    
    if edit_record.external_normal_payroll_title is not None:
        params['normal_payroll_title'] = edit_record.external_normal_payroll_title
    
    if edit_record.external_note16 is not None:
        params['note16'] = edit_record.external_note16
    
    if edit_record.external_note17 is not None:
        params['note17'] = edit_record.external_note17
    
    # 过滤掉None值的参数
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    logger.debug(f"构建edit_order参数完成 - 工单编号: {edit_record.external_roll_number}, "
                f"参数数量: {len(filtered_params)}")
    
    return filtered_params


def trigger_sync_edit_order(edit_record_id: int, delay: int = 0) -> Optional[str]:
    """触发编辑工单同步任务
    
    Args:
        edit_record_id: BaseEditRecord记录ID
        delay: 延迟执行秒数，默认立即执行
        
    Returns:
        str: 任务ID，如果触发失败返回None
    """
    try:
        if delay > 0:
            # 延迟执行
            task_result = sync_edit_order.apply_async(
                args=[edit_record_id],
                countdown=delay
            )
        else:
            # 立即执行
            task_result = sync_edit_order.delay(edit_record_id)
        
        task_id = task_result.id
        logger.info(f"编辑工单同步任务已触发 - 任务ID: {task_id}, 编辑记录ID: {edit_record_id}, "
                   f"延迟: {delay}秒")
        
        return task_id
        
    except Exception as e:
        logger.error(f"触发编辑工单同步任务失败 - 编辑记录ID: {edit_record_id}, 错误: {str(e)}", 
                    exc_info=True)
        return None


def get_sync_task_status(task_id: str) -> Dict[str, Any]:
    """获取同步任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        Dict[str, Any]: 任务状态信息
    """
    try:
        from celery import current_app
        
        task_result = current_app.AsyncResult(task_id)
        
        status_info = {
            'task_id': task_id,
            'status': task_result.status,
            'ready': task_result.ready(),
            'successful': task_result.successful() if task_result.ready() else None,
            'failed': task_result.failed() if task_result.ready() else None,
            'result': None,
            'error': None
        }
        
        if task_result.ready():
            if task_result.successful():
                status_info['result'] = task_result.result
            elif task_result.failed():
                status_info['error'] = str(task_result.info)
        
        return status_info
        
    except Exception as e:
        logger.error(f"获取任务状态失败 - 任务ID: {task_id}, 错误: {str(e)}")
        return {
            'task_id': task_id,
            'status': 'UNKNOWN',
            'error': f"获取状态失败: {str(e)}"
        }