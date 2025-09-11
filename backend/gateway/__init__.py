# -*- coding: utf-8 -*-

"""
平台网关SDK
简化与使用cookie + session认证的外部平台的集成
"""

__version__ = '1.0.0'
__author__ = 'igwen6w@gmail.com'

from .exceptions import (
    GatewayError,
    AuthenticationError,
    SessionExpiredError,
    PlatformUnavailableError,
    CaptchaError,
    PlatformAPIError,
    ConfigurationError,
)
from .api_wrappers import (
    PlatformAPI,
    get_api_instance,
    reset_api_instance,
    keepalive,
    get_pending_disposal_order_list,
    edit_order,
    get_order_detail,
    refresh_session,
    custom_request,
    batch_request,
    upload_file,
    download_file,
    get_api_statistics,
    health_check,
)
from .services import SessionManager
from .config import get_gateway_config
from .tasks import (
    execute_keepalive_now,
    execute_health_check_now, 
    execute_cleanup_now,
)
from .celery_config import (
    get_gateway_celery_config,
    validate_celery_config,
)

__all__ = [
    # 异常类
    'GatewayError',
    'AuthenticationError', 
    'SessionExpiredError',
    'PlatformUnavailableError',
    'CaptchaError',
    'PlatformAPIError',
    'ConfigurationError',
    # API封装类
    'PlatformAPI',
    'get_api_instance',
    'reset_api_instance',
    # 便捷函数
    'keepalive',
    'get_pending_disposal_order_list',
    'edit_order',
    'get_order_detail',
    'refresh_session',
    'custom_request',
    'batch_request',
    'upload_file',
    'download_file',
    'get_api_statistics',
    'health_check',
    # 核心组件
    'SessionManager',
    'get_gateway_config',
    # Celery任务
    'execute_keepalive_now',
    'execute_health_check_now',
    'execute_cleanup_now',
    'get_gateway_celery_config',
    'validate_celery_config',
]