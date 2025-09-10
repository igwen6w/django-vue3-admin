# -*- coding: utf-8 -*-

"""
维护认证状态任务
"""

import logging
import time
from typing import Dict, Any
from celery import shared_task

from external_platform.models import PlatformEndpoint
from external_platform.choices import PlatformAuthStatus
from external_platform.services.auth_service import AuthService
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.services.request_log import log_status_check_request
from external_platform.utils import get_platform_config, get_task_config
from external_platform.tasks.utils import handle_session_expiry

logger = logging.getLogger(__name__)


@shared_task
def maintain_auth_status_task() -> Dict[str, Any]:
    """维护认证状态的定时任务"""
    logger.info("开始执行认证状态维护任务")
    
    start_time = time.time()
    result = {
        'checked_count': 0,
        'refreshed_count': 0,
        'expired_count': 0,
        'error_count': 0
    }
    
    try:
        # 清理已过期的会话
        expired_count = AuthService.cleanup_expired_sessions()
        result['expired_count'] = expired_count
        
        # 获取即将过期的会话
        config = get_task_config('maintain_auth_status')
        refresh_before_hours = config.get('refresh_before_hours', 2)
        near_expiry_sessions = AuthService.get_sessions_near_expiry(refresh_before_hours)
        
        result['checked_count'] = len(near_expiry_sessions)
        
        # 触发刷新任务
        for session in near_expiry_sessions:
            try:
                # 请求 API 端点，检查登录状态
                # 使用 PlatformEndpoint endpoint_type 为 check_status 的端点来检查鉴权状态
                # response.res.card_number 为空时则表示会话过期
                
                # 获取状态检查端点
                try:
                    check_endpoint = PlatformEndpoint.objects.get(
                        platform=session.platform,
                        endpoint_type='check_status'
                    )
                except PlatformEndpoint.DoesNotExist:
                    logger.warning(f"平台 {session.platform.sign} 未配置状态检查端点")
                    continue
                
                # 获取平台配置
                platform_config = get_platform_config(session.platform.sign)
                if not platform_config:
                    logger.error(f"获取平台配置失败: {session.platform.sign}")
                    continue
                
                # 初始化客户端
                client = ExternalPlatformClient(platform_config['base_url'])
                
                try:
                    # 从会话中获取认证信息
                    auth_data = session.auth or {}
                    cookies = auth_data.get('cookies', {})
                    
                    # 发送状态检查请求
                    success, response_data, error_msg = client.make_authenticated_request(
                        method=check_endpoint.http_method,
                        endpoint=check_endpoint.path,
                        cookies=cookies
                    )
                    
                    # 记录请求日志
                    log_status_check_request(session, check_endpoint, success, response_data, error_msg)
                    
                    if success and response_data:
                        # 首先检查是否为会话失效响应
                        if handle_session_expiry(response_data, session, session.platform.sign):
                            # 会话失效已处理，无需进一步检查
                            pass
                        else:
                            # 检查响应中的 card_number 字段
                            res_data = response_data.get('res', {})
                            card_number = res_data.get('card_number', '')
                            
                            if not card_number:
                                # card_number 为空表示会话过期，更新会话状态
                                session.status = PlatformAuthStatus.EXPIRED
                                session.save(update_fields=['status', 'update_time'])
                                logger.info(f"会话已过期（card_number为空） - 会话ID: {session.id}, "
                                           f"平台: {session.platform.sign}, 账户: {session.account}")
                                
                                # 触发重新登录任务
                                login_task_id = AuthService.trigger_login_task(session.platform.sign)
                                if login_task_id:
                                    logger.info(f"已触发重新登录任务 - 登录任务ID: {login_task_id}, "
                                               f"平台: {session.platform.sign}")
                                else:
                                    logger.error(f"触发重新登录失败 - 平台: {session.platform.sign}")
                            else:
                                logger.info(f"会话状态正常 - 会话ID: {session.id}, "
                                           f"平台: {session.platform.sign}, 账户: {session.account}, "
                                           f"card_number: {card_number}")
                    else:
                        logger.warning(f"状态检查失败 - 会话ID: {session.id}, "
                                     f"错误: {error_msg}")
                
                finally:
                    client.close()

                logger.info(f"会话状态检查完成 - 会话ID: {session.id}, "
                           f"平台: {session.platform.sign}, 账户: {session.account}, "
                           f"过期时间: {session.expire_time}")
                result['refreshed_count'] += 1
                
            except Exception as e:
                logger.error(f"处理即将过期会话失败 - 会话ID: {session.id}, "
                            f"错误: {str(e)}", exc_info=True)
                result['error_count'] += 1
        
        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"认证状态维护任务完成 - 耗时: {execution_time}ms, "
                   f"检查: {result['checked_count']}, 刷新: {result['refreshed_count']}, "
                   f"过期: {result['expired_count']}, 错误: {result['error_count']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"认证状态维护任务异常: {str(e)}"
        logger.error(f"认证状态维护任务异常 - 耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        result['error_count'] += 1
        return result