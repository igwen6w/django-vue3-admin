# -*- coding: utf-8 -*-

"""
任务工具函数
"""

import logging
from typing import Dict, Any, Optional
from django.db import transaction

from external_platform.models import AuthSession
from external_platform.choices import PlatformAuthStatus
from external_platform.services.auth_service import AuthService

logger = logging.getLogger(__name__)


def handle_session_expiry(response_data: Dict[str, Any], session: AuthSession, 
                         platform_sign: str, task_self=None, 
                         retry_delay: int = 60) -> bool:
    """
    检查并处理会话失效响应
    
    Args:
        response_data: API响应数据
        session: 当前认证会话
        platform_sign: 平台标识
        task_self: Celery任务实例（用于重试）
        retry_delay: 重试延迟秒数
        
    Returns:
        bool: True表示检测到会话失效，False表示会话正常
        
    Raises:
        Exception: 当需要重试任务时抛出异常
    """
    # 检查是否为会话失效响应
    if (response_data.get('status') == 'fail' and 
        response_data.get('des') == 'session失效' and 
        response_data.get('res') == ''):
        
        logger.warning(f"检测到会话失效 - 会话ID: {session.id}, "
                      f"平台: {platform_sign}")
        
        # 更新会话状态为过期
        with transaction.atomic():
            session.status = PlatformAuthStatus.EXPIRED
            session.save(update_fields=['status', 'update_time'])
        
        logger.info(f"已更新会话状态为过期 - 会话ID: {session.id}")
        
        # 触发重新登录任务
        login_task_id = AuthService.trigger_login_task(platform_sign)
        
        if login_task_id:
            logger.info(f"已触发重新登录任务 - 登录任务ID: {login_task_id}, "
                       f"平台: {platform_sign}")
            
            # 如果提供了任务实例且还有重试次数，则重试任务
            if task_self and task_self.request.retries < task_self.max_retries:
                task_id = task_self.request.id
                logger.info(f"会话失效，将在登录完成后重试 - 任务ID: {task_id}, "
                           f"重试次数: {task_self.request.retries + 1}, "
                           f"延迟: {retry_delay}秒")
                
                error_msg = f"会话失效已触发重新登录，任务将重试 - 登录任务ID: {login_task_id}"
                raise task_self.retry(countdown=retry_delay, exc=Exception(error_msg))
            
        else:
            logger.error(f"触发重新登录失败 - 平台: {platform_sign}")
        
        return True
    
    return False