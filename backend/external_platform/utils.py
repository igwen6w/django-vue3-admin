# -*- coding: utf-8 -*-

"""
外部平台工具函数
"""

import logging
from typing import Dict, Any, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


def setup_external_platform_logging():
    """设置外部平台模块的日志配置"""
    
    # 获取或创建logger
    external_logger = logging.getLogger('external_platform')
    
    # 使用 Django 的默认日志级别
    # 如果没有处理器，添加控制台处理器
    if not external_logger.handlers:
        console_handler = logging.StreamHandler()
        
        # 设置格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        external_logger.addHandler(console_handler)
    
    logger.info("外部平台日志配置完成")


def log_api_request(platform_sign: str, account: str, endpoint: str, 
                   method: str, success: bool, response_time_ms: int,
                   error_msg: Optional[str] = None, 
                   additional_info: Optional[Dict] = None):
    """记录API请求日志
    
    Args:
        platform_sign: 平台标识
        account: 账户名
        endpoint: 端点
        method: HTTP方法
        success: 是否成功
        response_time_ms: 响应时间(毫秒)
        error_msg: 错误信息
        additional_info: 额外信息
    """
    log_data = {
        'platform': platform_sign,
        'account': account,
        'endpoint': endpoint,
        'method': method,
        'success': success,
        'response_time_ms': response_time_ms
    }
    
    if error_msg:
        log_data['error'] = error_msg
    
    if additional_info:
        log_data.update(additional_info)
    
    if success:
        logger.info(f"API请求成功 - {log_data}")
    else:
        logger.error(f"API请求失败 - {log_data}")


def get_platform_config(platform_sign: str) -> dict:
    """获取平台配置
    
    Args:
        platform_sign: 平台标识
        
    Returns:
        平台配置字典
    """
    from external_platform.models import Platform, PlatformEndpoint, PlatformConfig
    
    try:
        platform = Platform.objects.get(sign=platform_sign, is_active=True)
        
        # 基础配置
        config = {
            'name': platform.name,
            'base_url': platform.base_url,
            'captcha_type': platform.captcha_type,
            'session_timeout_hours': platform.session_timeout_hours,
            'retry_limit': platform.retry_limit,
            'login_config': platform.login_config,
            'endpoints': {}
        }
        
        # 端点配置
        endpoints = PlatformEndpoint.objects.filter(platform=platform)
        for endpoint in endpoints:
            config['endpoints'][endpoint.endpoint_type] = endpoint.path
        
        # 额外配置
        extra_configs = PlatformConfig.objects.filter(platform=platform)
        for extra_config in extra_configs:
            config[extra_config.config_key] = extra_config.config_value
        
        return config
        
    except Platform.DoesNotExist:
        logger.warning(f"未找到平台配置: {platform_sign}")
        return {}


def get_platform_instance(platform_sign: str):
    """获取平台实例
    
    Args:
        platform_sign: 平台标识
        
    Returns:
        Platform实例或None
    """
    from external_platform.models import Platform
    
    try:
        return Platform.objects.get(sign=platform_sign, is_active=True)
    except Platform.DoesNotExist:
        logger.warning(f"未找到平台: {platform_sign}")
        return None


def get_task_config(task_name: str) -> dict:
    """获取任务配置
    
    Args:
        task_name: 任务名称
        
    Returns:
        任务配置字典
    """
    from django.conf import settings
    task_config = getattr(settings, 'EXTERNAL_PLATFORM_TASK_CONFIG', {})
    return task_config.get(task_name, {})

