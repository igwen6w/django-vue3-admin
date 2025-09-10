# -*- coding: utf-8 -*-

"""
平台网关SDK异常类
定义了网关操作中可能遇到的各种异常类型
"""

import logging

logger = logging.getLogger(__name__)


class GatewayError(Exception):
    """网关基础异常类
    
    所有网关相关异常的基类，提供统一的异常处理接口
    """
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """初始化网关异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            details: 错误详细信息字典
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        
        # 记录异常日志
        logger.error(f"{self.__class__.__name__}: {message}", extra={
            'error_code': self.error_code,
            'details': self.details
        })
    
    def __str__(self):
        return f"[{self.error_code}] {self.message}"
    
    def to_dict(self):
        """转换为字典格式，便于序列化"""
        return {
            'error_type': self.__class__.__name__,
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details
        }


class AuthenticationError(GatewayError):
    """认证失败异常
    
    当用户名密码错误、认证服务器拒绝等认证相关问题时抛出
    """
    
    def __init__(self, message: str = "认证失败", username: str = None, **kwargs):
        """初始化认证异常
        
        Args:
            message: 错误消息
            username: 认证失败的用户名
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if username:
            details['username'] = username
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.username = username


class SessionExpiredError(GatewayError):
    """会话过期异常
    
    当检测到会话已过期需要重新认证时抛出
    """
    
    def __init__(self, message: str = "会话已过期", session_id: str = None, **kwargs):
        """初始化会话过期异常
        
        Args:
            message: 错误消息
            session_id: 过期的会话ID
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if session_id:
            details['session_id'] = session_id
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.session_id = session_id


class PlatformUnavailableError(GatewayError):
    """平台不可用异常
    
    当外部平台服务不可达、维护中或响应超时时抛出
    """
    
    def __init__(self, message: str = "外部平台不可用", platform_url: str = None, 
                 status_code: int = None, **kwargs):
        """初始化平台不可用异常
        
        Args:
            message: 错误消息
            platform_url: 平台URL
            status_code: HTTP状态码
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if platform_url:
            details['platform_url'] = platform_url
        if status_code:
            details['status_code'] = status_code
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.platform_url = platform_url
        self.status_code = status_code


class CaptchaError(GatewayError):
    """验证码处理异常
    
    当验证码识别失败、验证码服务不可用等验证码相关问题时抛出
    """
    
    def __init__(self, message: str = "验证码处理失败", pic_id: str = None, 
                 captcha_type: int = None, retry_count: int = None, **kwargs):
        """初始化验证码异常
        
        Args:
            message: 错误消息
            pic_id: 超级鹰图片ID，用于报告错误
            captcha_type: 验证码类型
            retry_count: 重试次数
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if pic_id:
            details['pic_id'] = pic_id
        if captcha_type:
            details['captcha_type'] = captcha_type
        if retry_count is not None:
            details['retry_count'] = retry_count
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.pic_id = pic_id
        self.captcha_type = captcha_type
        self.retry_count = retry_count


class PlatformAPIError(GatewayError):
    """平台API调用异常
    
    当平台API返回错误响应、数据格式异常等API调用问题时抛出
    """
    
    def __init__(self, message: str = "平台API调用失败", status_code: int = None, 
                 response_data: dict = None, api_endpoint: str = None, **kwargs):
        """初始化平台API异常
        
        Args:
            message: 错误消息
            status_code: HTTP状态码
            response_data: 响应数据
            api_endpoint: API端点
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if status_code:
            details['status_code'] = status_code
        if response_data:
            details['response_data'] = response_data
        if api_endpoint:
            details['api_endpoint'] = api_endpoint
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response_data = response_data
        self.api_endpoint = api_endpoint


class ConfigurationError(GatewayError):
    """配置错误异常
    
    当配置文件缺失、配置项不正确等配置相关问题时抛出
    """
    
    def __init__(self, message: str = "配置错误", config_key: str = None, 
                 config_section: str = None, **kwargs):
        """初始化配置异常
        
        Args:
            message: 错误消息
            config_key: 配置键名
            config_section: 配置段名
            **kwargs: 其他参数传递给父类
        """
        details = kwargs.get('details', {})
        if config_key:
            details['config_key'] = config_key
        if config_section:
            details['config_section'] = config_section
        kwargs['details'] = details
        
        super().__init__(message, **kwargs)
        self.config_key = config_key
        self.config_section = config_section


# 异常重试策略配置
RETRY_STRATEGIES = {
    # 网络超时: 指数退避重试
    'network_timeout': {
        'max_retries': 3,
        'base_delay': 1,  # 秒
        'backoff_factor': 2,
        'max_delay': 60
    },
    
    # 会话过期: 立即重试一次
    'session_expired': {
        'max_retries': 1,
        'base_delay': 0,
        'backoff_factor': 1,
        'max_delay': 0
    },
    
    # 验证码错误: 立即重试
    'captcha_error': {
        'max_retries': 3,
        'base_delay': 0,
        'backoff_factor': 1,
        'max_delay': 0
    },
    
    # 服务器错误(5xx): 指数退避重试
    'server_error': {
        'max_retries': 3,
        'base_delay': 5,
        'backoff_factor': 2,
        'max_delay': 120
    },
    
    # 认证失败: 不重试
    'authentication_failed': {
        'max_retries': 0,
        'base_delay': 0,
        'backoff_factor': 1,
        'max_delay': 0
    }
}


def get_retry_strategy(error_type: str) -> dict:
    """获取指定错误类型的重试策略
    
    Args:
        error_type: 错误类型字符串
        
    Returns:
        重试策略字典
    """
    return RETRY_STRATEGIES.get(error_type, RETRY_STRATEGIES['network_timeout'])


def should_retry(exception: Exception, attempt: int = 1) -> bool:
    """判断异常是否应该重试
    
    Args:
        exception: 异常实例
        attempt: 当前尝试次数
        
    Returns:
        是否应该重试
    """
    # 根据异常类型确定重试策略
    if isinstance(exception, AuthenticationError):
        strategy = get_retry_strategy('authentication_failed')
    elif isinstance(exception, SessionExpiredError):
        strategy = get_retry_strategy('session_expired')
    elif isinstance(exception, CaptchaError):
        strategy = get_retry_strategy('captcha_error')
    elif isinstance(exception, PlatformAPIError):
        if exception.status_code and 500 <= exception.status_code < 600:
            strategy = get_retry_strategy('server_error')
        else:
            return False  # 4xx错误通常不重试
    elif isinstance(exception, PlatformUnavailableError):
        strategy = get_retry_strategy('network_timeout')
    else:
        return False  # 其他异常不重试
    
    return attempt <= strategy['max_retries']


def calculate_retry_delay(exception: Exception, attempt: int) -> float:
    """计算重试延迟时间
    
    Args:
        exception: 异常实例
        attempt: 当前尝试次数
        
    Returns:
        延迟时间（秒）
    """
    # 根据异常类型获取重试策略
    if isinstance(exception, AuthenticationError):
        strategy = get_retry_strategy('authentication_failed')
    elif isinstance(exception, SessionExpiredError):
        strategy = get_retry_strategy('session_expired')
    elif isinstance(exception, CaptchaError):
        strategy = get_retry_strategy('captcha_error')
    elif isinstance(exception, PlatformAPIError):
        if exception.status_code and 500 <= exception.status_code < 600:
            strategy = get_retry_strategy('server_error')
        else:
            strategy = get_retry_strategy('network_timeout')
    elif isinstance(exception, PlatformUnavailableError):
        strategy = get_retry_strategy('network_timeout')
    else:
        strategy = get_retry_strategy('network_timeout')
    
    # 计算指数退避延迟
    delay = strategy['base_delay'] * (strategy['backoff_factor'] ** (attempt - 1))
    return min(delay, strategy['max_delay'])