# -*- coding: utf-8 -*-

"""
批量获取工单任务
"""

import logging
import time
from datetime import timedelta
from typing import Dict, Any
from celery import shared_task
from django.utils import timezone

from external_platform.models import Platform, AuthSession, PlatformEndpoint
from external_platform.choices import PlatformAuthStatus
from external_platform.services.auth_service import AuthService
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.services.request_log import log_workorder_list_request
from external_platform.utils import get_platform_config, get_task_config
from external_platform.tasks.utils import handle_session_expiry
from external_platform.tasks import fetch_single_workorder_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def batch_fetch_workorders_task(self) -> Dict[str, Any]:
    """定时任务:批量获取市中心系统工单
    
    任务执行流程：
    0. 从 PlatformEndpoint endpoint_type = workorder_list 获取API端点和请求参数
    1. 构建请求参数
    2. 获取已鉴权会话句柄
    3. 请求端点获取工单列表
    4. 处理列表中的每个记录，创建获取单个工单详情任务
    5. 结束任务
    
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    platform_sign = 'city_center_workorder'
    
    logger.info(f"开始执行批量获取工单任务 - 任务ID: {task_id}, 平台: {platform_sign}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'task_id': task_id,
        'fetched_count': 0,
        'created_tasks': 0,
        'saved_records': 0,
        'skipped_records': 0,
        'error': None
    }
    
    try:
        # 步骤0: 获取平台和工单列表端点配置
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        try:
            workorder_endpoint = PlatformEndpoint.objects.get(
                platform=platform,
                endpoint_type='workorder_list'
            )
        except PlatformEndpoint.DoesNotExist:
            error_msg = f"平台 {platform_sign} 未配置工单列表端点"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 步骤1: 构建请求参数
        base_payload = workorder_endpoint.payload or {}
        
        # 获取当前时间范围（默认获取最近30天的工单）
        end_time = timezone.now()
        start_time_param = end_time - timedelta(days=30)
        
        request_payload = {
            **base_payload,
            'search_start_time': start_time_param.strftime('%Y-%m-%d %H:%M:%S'),
            'search_end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'page': 1,
            'pagesize': 50  # 每页获取50条记录
        }
        
        logger.info(f"构建请求参数完成 - 时间范围: {request_payload['search_start_time']} 到 {request_payload['search_end_time']}")
        
        # 步骤2: 获取已鉴权会话句柄
        try:
            active_session = AuthSession.objects.filter(
                platform=platform,
                status=PlatformAuthStatus.ACTIVE,
                expire_time__gt=timezone.now()
            ).first()
            
            if not active_session:
                # 发起登录
                AuthService.trigger_login_task(platform_sign)
                # 记录日志
                error_msg = "未找到有效的认证会话，请先执行登录任务"
                logger.warning(error_msg)
                result['error'] = error_msg
                return result
                
        except Exception as e:
            error_msg = f"获取认证会话失败: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 步骤3: 请求端点获取工单列表
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
            
            # 发送工单列表请求
            success, response_data, error_msg = client.make_authenticated_request(
                method=workorder_endpoint.http_method,
                endpoint=workorder_endpoint.path,
                cookies=cookies,
                data=request_payload if workorder_endpoint.http_method == 'POST' else None,
                params=request_payload if workorder_endpoint.http_method == 'GET' else None
            )
            
            # 记录请求日志
            log_workorder_list_request(active_session, workorder_endpoint, success, response_data, error_msg, request_payload)
            
            # 检查会话失效响应
            if success and response_data:
                try:
                    retry_delay = get_task_config('batch_fetch_workorders_task').get('retry_delay', 300)
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
                error_msg = f"获取工单列表失败: {error_msg}"
                logger.error(error_msg)
                result['error'] = error_msg
                return result
            
            # 步骤4: 处理工单列表数据并存储到数据库
            workorder_list = []
            if response_data and 'res' in response_data:
                res_data = response_data['res']
                # 根据实际数据结构，工单列表在 tbody 字段中
                if isinstance(res_data, dict) and 'tbody' in res_data:
                    workorder_list = res_data['tbody']
                elif isinstance(res_data, dict) and 'list' in res_data:
                    workorder_list = res_data['list']
                elif isinstance(res_data, list):
                    workorder_list = res_data
            
            result['fetched_count'] = len(workorder_list)
            logger.info(f"获取到工单列表 - 数量: {result['fetched_count']}")
            
            # 步骤5: 存储工单数据到数据库并创建同步工单数据任务
            from work_order.models import Meta as WorkOrderMeta
            
            created_tasks = 0
            saved_records = 0
            skipped_records = 0
            
            for workorder in workorder_list:
                try:
                    # 根据实际数据结构，工单ID在 id 字段中
                    workorder_id = workorder.get('id')
                    if not workorder_id:
                        logger.warning(f"工单缺少ID字段 - 工单数据: {workorder}")
                        continue
                    
                    fetch_single_workorder_task.delay(
                        platform_sign=platform_sign,
                        workorder_id=workorder_id,
                        batch_task_id=task_id
                    )
                    created_tasks += 1
                    logger.debug(f"创建工单详情任务 - 工单ID: {workorder_id}, 工单类型: {workorder.get('payroll_type', '')}")
                    
                    
                except Exception as e:
                    logger.error(f"处理工单数据失败 - 工单ID: {workorder.get('id', 'unknown')}, 错误: {str(e)}", exc_info=True)
            
            result['created_tasks'] = created_tasks
            result['saved_records'] = saved_records
            result['skipped_records'] = skipped_records
            result['success'] = True
            
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"批量获取工单任务完成 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                       f"获取数量: {result['fetched_count']}, 保存: {result['saved_records']}, "
                       f"跳过: {result['skipped_records']}, 创建任务: {result['created_tasks']}")
            
        finally:
            client.close()
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"批量获取工单任务异常: {str(e)}"
        logger.error(f"批量获取工单任务异常 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                    f"错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('batch_fetch_workorders_task').get('retry_delay', 300)  # 5分钟后重试
            logger.info(f"批量获取工单任务重试 - 任务ID: {task_id}, 重试次数: {self.request.retries + 1}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result