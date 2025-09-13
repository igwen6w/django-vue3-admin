# -*- coding: utf-8 -*-

"""
获取单个工单详情任务

该模块负责获取单个工单的详细信息，使用gateway API获取数据，
并将原始数据保存到Meta模型中，然后触发同步任务。
"""

import logging
import time
from typing import Dict, Any, Optional
from celery import shared_task

from external_platform.utils import get_task_config
from external_platform.tasks.sync_data_2_base_order import sync_data_2_base_order
from gateway import get_order_detail
from utils.crypto import CryptoUtils

logger = logging.getLogger(__name__)

def _extract_ps_caption_current_from_order_step_chart(order_step_chart: list[dict[str, Any]]) -> Optional[str]:
    """从工单节点流程中提取当前节点
    
    Args:
        order_step_chart: 工单节点流程
        
    Returns:
        当前节点
    """
    for item in order_step_chart:
        if item.get('ps_caption_current'):
            return item.get('ps_caption_current')
    return None

def _extract_order_step_chart_from_response(response_data: Dict[str, Any]) -> Optional[Any]:
    """从响应数据中提取工单节点流程
    
    Args:
        response_data: API响应数据
        
    Returns:
        工单节点流程
    """
    return response_data.get('data', {})

def _extract_order_number_from_res(res: list[dict[str, Any]]) -> Optional[str]:
    """从res列表中提取工单编号
    
    Args:
        res: API响应数据
        
    Returns:
        工单编号
    """
    if not res or not isinstance(res, list):
        return None
    
    for item in res:
        if item.get('fd_name') == 'roll_number':
            return item.get('choice_value')
    return None

def _extract_order_detail_from_response(response_data: Dict[str, Any]) -> Optional[Any]:
    """从响应数据中提取工单详情
    
    Args:
        response_data: API响应数据
        
    Returns:
        工单详情的Python对象，如果找不到则返回None
    """
    if not response_data or not response_data.get('success'):
        return None
    
    data = response_data.get('data', {})
    
    # 检查是否有res字段
    if 'res' in data and isinstance(data['res'], list):
        # 直接返回res列表，让JSONField自动处理序列化
        return data['res']
    
    return None


def _validate_response_data(response_data: Dict[str, Any]) -> bool:
    """验证响应数据是否有效
    
    Args:
        response_data: API响应数据
        
    Returns:
        数据是否有效
    """
    if not response_data or not response_data.get('success'):
        return False
    
    data = response_data.get('data', {})
    
    # 检查是否有预期的数据结构
    if 'res' not in data:
        return False
    
    res = data['res']
    if not isinstance(res, list) or len(res) == 0:
        return False
    
    return True


def _get_task_config_with_defaults() -> Dict[str, Any]:
    """获取任务配置，包含默认值
    
    Returns:
        任务配置字典
    """
    try:
        config = get_task_config('fetch_single_workorder_task')
    except Exception:
        config = {}
    
    defaults = {
        'retry_delay': 60,
        'timeout': 30
    }
    
    return {**defaults, **config}


@shared_task(bind=True, max_retries=3)
def fetch_single_workorder_task(self, platform_sign: str, workorder_id: str, batch_task_id: Optional[str] = None) -> Dict[str, Any]:
    """获取单个工单详情任务
    
    使用gateway API获取工单详情，将完整的响应数据保存到Meta模型中，
    然后触发同步任务将数据转换到Base模型。
    
    Args:
        platform_sign: 平台标识
        workorder_id: 工单ID
        batch_task_id: 批量任务ID（可选）
        
    Returns:
        任务执行结果字典，包含成功状态、Meta记录ID和错误信息
    """
    task_id = self.request.id
    
    # 获取配置
    config = _get_task_config_with_defaults()
    
    logger.info(f"开始获取单个工单详情 - 任务ID: {task_id}, 平台: {platform_sign}, 工单ID: {workorder_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'workorder_id': workorder_id,
        'task_id': task_id,
        'batch_task_id': batch_task_id,
        'meta_record_id': None,
        'sync_task_triggered': False,
        'skipped': False,
        'skip_reason': None,
        'error': None,
        'execution_time_ms': 0
    }
    
    try:
        # 调用gateway API获取工单详情
        logger.debug(f"调用get_order_detail - 工单ID: {workorder_id}")
        response_data = get_order_detail(workorder_id)
        
        # 检查API响应
        if not response_data:
            error_msg = "获取工单详情失败：API返回空响应"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        if not response_data.get('success', False):
            error_msg = f"获取工单详情失败：{response_data.get('error', '未知错误')}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 验证响应数据结构
        if not _validate_response_data(response_data):
            error_msg = "获取工单详情失败：响应数据格式无效"
            logger.error(f"{error_msg} - 响应数据: {response_data}")
            result['error'] = error_msg
            return result
        
        # res list
        raw_data = _extract_order_detail_from_response(response_data)
        order_number = _extract_order_number_from_res(raw_data)

        # 获取工单节点流程
        from gateway import get_order_step_chart
        order_step_chart_response = get_order_step_chart(order_number)
        order_step_chart = _extract_order_step_chart_from_response(order_step_chart_response)
        if not order_step_chart:
            error_msg = "获取工单节点流程失败"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 合并工单节点流程和工单详情
        raw_data.extend({'order_step_chart': order_step_chart})
        raw_data.extend({'ps_caption_current': _extract_ps_caption_current_from_order_step_chart(order_step_chart)})


        # 保存原始工单数据到Meta模型
        from work_order.models import Meta as WorkOrderMeta
        
        try:            
            sync_task_id = task_id
            pull_task_id = batch_task_id

            # 计算版本号
            import json
            raw_data_str = json.dumps(raw_data, ensure_ascii=False, sort_keys=True) if raw_data else ''
            current_version = CryptoUtils.md5(raw_data_str.encode('utf-8')).hexdigest()
            external_id_int = int(workorder_id) if workorder_id.isdigit() else 0
            
            # 检查是否已存在相同external_id的最新记录，且version相同
            existing_record = WorkOrderMeta.objects.filter(
                external_id=external_id_int
            ).order_by('-create_time').first()
            
            if existing_record and existing_record.version == current_version:
                logger.info(f"工单数据未变化，跳过插入 - 工单ID: {workorder_id}, 版本: {current_version}")
                result['meta_record_id'] = existing_record.id
                result['skipped'] = True
                result['skip_reason'] = 'version_unchanged'
                
                # 对于跳过的记录，不触发同步任务
                logger.info(f"数据未变化，跳过同步任务 - 工单ID: {workorder_id}, Meta记录ID: {existing_record.id}")
            else:
                # 创建Meta记录
                meta_record = WorkOrderMeta.objects.create(
                    version=current_version,
                    source_system=platform_sign,
                    sync_task_id=str(sync_task_id),
                    raw_data=raw_data,
                    pull_task_id=str(pull_task_id),
                    external_id=external_id_int,
                    order_number=order_number,
                )
                
                result['meta_record_id'] = meta_record.id
                
                logger.info(f"保存原始工单数据成功 - 工单ID: {workorder_id}, Meta记录ID: {meta_record.id}")
                
                # 触发同步到Base表的任务
                try:
                    sync_data_2_base_order.delay(meta_record.id)
                    result['sync_task_triggered'] = True
                    logger.info(f"已触发同步任务 - Meta记录ID: {meta_record.id}")
                except Exception as e:
                    logger.warning(f"触发同步任务失败 - Meta记录ID: {meta_record.id}, 错误: {e}")
                    # 同步任务触发失败不影响主任务成功
                
        except Exception as e:
            error_msg = f"保存工单数据到Meta表失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            result['error'] = error_msg
            return result
        
        # 任务执行成功
        result['success'] = True
        
        execution_time = int((time.time() - start_time) * 1000)
        result['execution_time_ms'] = execution_time
        
        logger.info(f"获取单个工单详情完成 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                   f"Meta记录ID: {result['meta_record_id']}, 耗时: {execution_time}ms")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        result['execution_time_ms'] = execution_time
        error_msg = f"获取单个工单详情异常: {str(e)}"
        
        logger.error(f"获取单个工单详情异常 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = config.get('retry_delay', 60)
            logger.info(f"准备重试获取单个工单详情 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                       f"重试次数: {self.request.retries + 1}/{self.max_retries}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result