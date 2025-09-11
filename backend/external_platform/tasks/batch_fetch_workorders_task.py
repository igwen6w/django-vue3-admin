# -*- coding: utf-8 -*-

"""
批量获取工单任务

该模块负责定时从市中心系统批量获取待处置工单，
并为每个工单创建详情获取任务。
"""

import logging
import time
from typing import Dict, Any, List, Optional
from celery import shared_task

from external_platform.utils import get_task_config
from external_platform.tasks import fetch_single_workorder_task
from gateway import get_pending_disposal_order_list

logger = logging.getLogger(__name__)


def _extract_workorder_list(response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从API响应中提取工单列表
    
    Args:
        response_data: API响应数据
        
    Returns:
        工单列表
    """
    if not response_data or not response_data.get('success'):
        return []
    
    data = response_data.get('data', {})
    
    # 尝试不同的数据结构路径
    possible_paths = [
        ['res', 'tbody'],      # 标准表格数据格式
        ['res', 'list'],       # 列表格式
        ['res'],               # 直接数据格式
        ['tbody'],              # 简化表格格式
        ['list'],               # 简化列表格式
    ]
    
    for path in possible_paths:
        current_data = data
        for key in path:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                break
        else:
            # 所有路径都找到了
            if isinstance(current_data, list):
                return current_data
    
    # 如果data本身就是列表
    if isinstance(data, list):
        return data
    
    return []


def _validate_workorder(workorder: Dict[str, Any]) -> Optional[str]:
    """验证工单数据并返回工单ID
    
    Args:
        workorder: 工单数据
        
    Returns:
        工单ID，如果无效则返回None
    """
    if not isinstance(workorder, dict):
        return None
    
    # ID字段名
    id_fields = ['id']
    
    for field in id_fields:
        workorder_id = workorder.get(field)
        if workorder_id:
            return str(workorder_id)
    
    return None


def _get_task_config_with_defaults() -> Dict[str, Any]:
    """获取任务配置，包含默认值
    
    Returns:
        任务配置字典
    """
    try:
        config = get_task_config('batch_fetch_workorders_task')
    except Exception:
        config = {}
    
    defaults = {
        'page_size': 50,
        'max_pages': 10,
        'retry_delay': 300,
        'timeout': 30
    }
    
    return {**defaults, **config}


@shared_task(bind=True, max_retries=3)
def batch_fetch_workorders_task(self, page: int = 1, page_size: Optional[int] = None) -> Dict[str, Any]:
    """定时任务：批量获取市中心系统待处置工单
    
    任务执行流程：
    1. 调用gateway API获取待处置工单列表
    2. 解析响应数据，提取工单信息
    3. 为每个有效工单创建详情获取任务
    4. 返回执行结果统计
    
    Args:
        page: 页码，默认为1
        page_size: 每页数量，如果不指定则使用配置中的默认值
    
    Returns:
        任务执行结果字典，包含成功状态、统计信息和错误信息
    """
    task_id = self.request.id
    platform_sign = 'city_center_workorder'
    
    # 获取配置
    config = _get_task_config_with_defaults()
    if page_size is None:
        page_size = config['page_size']
    
    logger.info(f"开始执行批量获取工单任务 - 任务ID: {task_id}, 平台: {platform_sign}, "
               f"页码: {page}, 每页: {page_size}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'task_id': task_id,
        'page': page,
        'page_size': page_size,
        'fetched_count': 0,
        'valid_count': 0,
        'created_tasks': 0,
        'skipped_count': 0,
        'error': None,
        'execution_time_ms': 0
    }
    
    try:
        # 调用gateway API获取待处置工单列表
        logger.debug(f"调用get_pending_disposal_order_list - 页码: {page}, 每页: {page_size}")
        response_data = get_pending_disposal_order_list(page=page, page_size=page_size)
        
        # 检查API响应
        if not response_data:
            error_msg = "获取工单列表失败：API返回空响应"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        if not response_data.get('success', False):
            error_msg = f"获取工单列表失败：{response_data.get('error', '未知错误')}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 提取工单列表
        workorder_list = _extract_workorder_list(response_data)
        result['fetched_count'] = len(workorder_list)
        
        logger.info(f"成功获取工单列表 - 数量: {result['fetched_count']}")
        
        if not workorder_list:
            logger.info("没有获取到工单数据，任务结束")
            result['success'] = True
            return result
        
        # 处理每个工单，创建详情获取任务
        created_tasks = 0
        valid_count = 0
        skipped_count = 0
        
        for i, workorder in enumerate(workorder_list):
            try:
                # 验证工单数据
                workorder_id = _validate_workorder(workorder)
                if not workorder_id:
                    logger.warning(f"跳过无效工单 [{i+1}/{len(workorder_list)}] - 数据: {workorder}")
                    skipped_count += 1
                    continue
                
                valid_count += 1
                
                # 创建工单详情获取任务
                fetch_single_workorder_task.delay(
                    platform_sign=platform_sign,
                    workorder_id=workorder_id,
                    batch_task_id=task_id
                )
                created_tasks += 1
                
                logger.debug(f"创建工单详情任务 [{valid_count}/{len(workorder_list)}] - "
                           f"工单ID: {workorder_id}, 类型: {workorder.get('payroll_type', 'N/A')}")
                
            except Exception as e:
                skipped_count += 1
                logger.error(f"处理工单失败 [{i+1}/{len(workorder_list)}] - "
                           f"工单ID: {workorder.get('id', 'unknown')}, 错误: {e}", exc_info=True)
        
        # 更新结果
        result.update({
            'valid_count': valid_count,
            'created_tasks': created_tasks,
            'skipped_count': skipped_count,
            'success': True
        })
        
        execution_time = int((time.time() - start_time) * 1000)
        result['execution_time_ms'] = execution_time
        
        logger.info(f"批量获取工单任务完成 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                   f"获取: {result['fetched_count']}, 有效: {result['valid_count']}, "
                   f"创建任务: {result['created_tasks']}, 跳过: {result['skipped_count']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        result['execution_time_ms'] = execution_time
        error_msg = f"批量获取工单任务异常: {str(e)}"
        
        logger.error(f"批量获取工单任务异常 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                    f"错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = config.get('retry_delay', 300)
            logger.info(f"准备重试批量获取工单任务 - 任务ID: {task_id}, "
                       f"重试次数: {self.request.retries + 1}/{self.max_retries}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result