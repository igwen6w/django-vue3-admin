# -*- coding: utf-8 -*-

"""
获取单个工单详情任务
"""

import logging
import time
from typing import Dict, Any
from celery import shared_task
from django.utils import timezone

from external_platform.models import Platform, AuthSession, PlatformEndpoint
from external_platform.choices import PlatformAuthStatus
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.services.request_log import log_workorder_detail_request
from external_platform.utils import get_platform_config, get_task_config
from external_platform.tasks.utils import handle_session_expiry
from external_platform.tasks.sync_data_2_base_order import sync_data_2_base_order

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_single_workorder_task(self, platform_sign: str, workorder_id: str, batch_task_id: str = None) -> Dict[str, Any]:
    """获取单个工单详情任务
    
    Args:
        platform_sign: 平台标识
        workorder_id: 工单ID
        batch_task_id: 批量任务ID（可选）
        
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    logger.info(f"开始获取单个工单详情 - 任务ID: {task_id}, 平台: {platform_sign}, 工单ID: {workorder_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'workorder_id': workorder_id,
        'task_id': task_id,
        'batch_task_id': batch_task_id,
        'error': None
    }
    
    try:
        # 获取平台配置
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 获取工单详情端点（假设端点类型为 workorder_detail）
        try:
            detail_endpoint = PlatformEndpoint.objects.get(
                platform=platform,
                endpoint_type='workorder_detail'
            )
        except PlatformEndpoint.DoesNotExist:
            error_msg = f"平台 {platform_sign} 未配置工单详情端点"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 获取认证会话
        try:
            active_session = AuthSession.objects.filter(
                platform=platform,
                status=PlatformAuthStatus.ACTIVE,
                expire_time__gt=timezone.now()
            ).first()
            
            if not active_session:
                error_msg = "未找到有效的认证会话"
                logger.warning(error_msg)
                result['error'] = error_msg
                return result
                
        except Exception as e:
            error_msg = f"获取认证会话失败: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 构建请求参数
        base_payload = detail_endpoint.payload or {}
        request_payload = {
            **base_payload,
            'act': 'payroll_view_module',
            'id': workorder_id,
            'module_name': '系统默认'
        }
        
        # 获取平台配置并发送请求
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"获取平台配置失败: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        client = ExternalPlatformClient(platform_config['base_url'])
        
        try:
            # 从会话中获取认证信息
            auth_data = active_session.auth or {}
            cookies = auth_data.get('cookies', {})
            
            # 发送工单详情请求
            success, response_data, error_msg = client.make_authenticated_request(
                method=detail_endpoint.http_method,
                endpoint=detail_endpoint.path,
                cookies=cookies,
                data=request_payload if detail_endpoint.http_method == 'POST' else None,
                params=request_payload if detail_endpoint.http_method == 'GET' else None
            )
            
            # 记录请求日志
            log_workorder_detail_request(active_session, detail_endpoint, success, response_data, error_msg, request_payload)
            
            # 检查会话失效响应
            if success and response_data:
                try:
                    retry_delay = get_task_config('fetch_single_workorder_task').get('retry_delay', 60)
                    if handle_session_expiry(response_data, active_session, platform_sign, 
                                           task_self=self, retry_delay=retry_delay):
                        # 如果检测到会话失效但无法重试，返回错误
                        error_msg = "会话失效且已达到最大重试次数或触发重新登录失败"
                        result['error'] = error_msg
                        return result
                except Exception as e:
                    # 如果是重试异常，重新抛出
                    if "会话失效已触发重新登录" in str(e):
                        raise
                    else:
                        error_msg = f"处理会话失效异常: {str(e)}"
                        logger.error(error_msg)
                        result['error'] = error_msg
                        return result
            
            if not success:
                error_msg = f"获取工单详情失败: {error_msg}"
                logger.error(error_msg)
                result['error'] = error_msg
                return result
            
            # 保存原始工单数据
            if response_data:
                from work_order.models import Meta as WorkOrderMeta
                
                # 创建原始工单记录
                meta_record = WorkOrderMeta.objects.create(
                    version='1.0',
                    source_system=platform_sign,
                    sync_task_id=int(task_id.replace('-', '')[:10], 16),  # 将任务ID转换为数字
                    raw_data=response_data,
                    pull_task_id=int(batch_task_id.replace('-', '')[:10], 16) if batch_task_id else 0
                )
                
                logger.info(f"保存原始工单成功 - 工单ID: {workorder_id}, 记录ID: {meta_record.id}")
                result['meta_record_id'] = meta_record.id
                
                # 触发同步到基础表的任务
                sync_data_2_base_order.delay(meta_record.id)
                logger.info(f"已触发同步任务 - Meta记录ID: {meta_record.id}")
            
            result['success'] = True
            
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"获取单个工单详情完成 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                       f"耗时: {execution_time}ms")
            
        finally:
            client.close()
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"获取单个工单详情异常: {str(e)}"
        logger.error(f"获取单个工单详情异常 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('fetch_single_workorder_task').get('retry_delay', 60)
            logger.info(f"获取单个工单详情重试 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                       f"重试次数: {self.request.retries + 1}, 延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result