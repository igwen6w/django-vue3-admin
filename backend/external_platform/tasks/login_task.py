# -*- coding: utf-8 -*-

"""
登录任务
"""

import logging
import time
from typing import Dict, Any
from celery import shared_task

from external_platform.models import Platform
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.utils import get_platform_config, get_task_config

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def login_task(self, platform_sign: str) -> Dict[str, Any]:
    """异步登录任务
    
    Args:
        platform_sign: 平台标识
        
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    logger.info(f"开始执行登录任务 - 任务ID: {task_id}, 平台: {platform_sign}")
    
    start_time = time.time()
    platform = None
    client = None
    
    try:
        # 获取平台配置
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"未找到平台配置: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 获取平台对象
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 初始化客户端
        client = ExternalPlatformClient(platform_config['base_url'])
        
        # 执行登录流程
        result = client.execute_complete_login_flow(
            task_id, platform, platform_config
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        if result['success']:
            logger.info(f"登录任务完成 - 任务ID: {task_id}, 平台: {platform_sign}, "
                       f"耗时: {execution_time}ms")
        else:
            logger.error(f"登录任务失败 - 任务ID: {task_id}, 平台: {platform_sign}, "
                        f"耗时: {execution_time}ms, 错误: {result['error']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"登录任务异常: {str(e)}"
        logger.error(f"登录任务异常 - 任务ID: {task_id}, 平台: {platform_sign}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('login_task').get('retry_delay', 60)
            logger.info(f"登录任务重试 - 任务ID: {task_id}, 重试次数: {self.request.retries + 1}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return {'success': False, 'error': error_msg}
    
    finally:
        if client:
            client.close()