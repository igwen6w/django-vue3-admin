# -*- coding: utf-8 -*-

"""
平台网关SDK
简化与使用cookie + session认证的外部平台的集成
"""

__version__ = '1.0.0'
__author__ = 'Django Vue3 Admin Team'

from .exceptions import (
    GatewayError,
    AuthenticationError,
    SessionExpiredError,
    PlatformUnavailableError,
    CaptchaError,
    PlatformAPIError,
    ConfigurationError,
)

__all__ = [
    'GatewayError',
    'AuthenticationError', 
    'SessionExpiredError',
    'PlatformUnavailableError',
    'CaptchaError',
    'PlatformAPIError',
    'ConfigurationError',
]