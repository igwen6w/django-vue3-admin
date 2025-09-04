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


def get_captcha_config() -> dict:
    """获取验证码配置
    
    Returns:
        验证码配置字典
    """
    from django.conf import settings
    return getattr(settings, 'CHAOJIYING_CONFIG', {})


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


def validate_platform_config(platform_config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """验证平台配置的完整性
    
    Args:
        platform_config: 平台配置字典
        
    Returns:
        (是否有效, 错误信息)
    """
    required_fields = ['name', 'base_url', 'endpoints']
    required_endpoints = ['captcha', 'login', 'check_status']
    
    # 检查必需字段
    for field in required_fields:
        if field not in platform_config:
            return False, f"缺少必需配置字段: {field}"
    
    # 检查端点配置
    endpoints = platform_config.get('endpoints', {})
    for endpoint in required_endpoints:
        if endpoint not in endpoints:
            return False, f"缺少必需端点配置: {endpoint}"
    
    # 检查URL格式
    base_url = platform_config.get('base_url', '')
    if not base_url.startswith(('http://', 'https://')):
        return False, "base_url必须以http://或https://开头"
    
    return True, None


def format_session_info(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """格式化会话信息用于API响应
    
    Args:
        session_data: 原始会话数据
        
    Returns:
        格式化后的会话信息
    """
    formatted_data = {}
    
    # 基本信息
    basic_fields = ['session_id', 'platform_sign', 'platform_name', 
                   'account', 'status', 'is_valid']
    
    for field in basic_fields:
        if field in session_data:
            formatted_data[field] = session_data[field]
    
    # 时间字段格式化
    time_fields = ['login_time', 'expire_time']
    for field in time_fields:
        if field in session_data and session_data[field]:
            if hasattr(session_data[field], 'isoformat'):
                formatted_data[field] = session_data[field].isoformat()
            else:
                formatted_data[field] = str(session_data[field])
    
    # 脱敏认证数据
    if 'auth_data' in session_data:
        formatted_data['has_auth_data'] = bool(session_data['auth_data'])
    
    return formatted_data


def get_retry_delay(attempt: int, base_delay: int = 60, max_delay: int = 300) -> int:
    """计算重试延迟时间（指数退避）
    
    Args:
        attempt: 重试次数
        base_delay: 基础延迟时间(秒)
        max_delay: 最大延迟时间(秒)
        
    Returns:
        延迟时间(秒)
    """
    delay = base_delay * (2 ** attempt)
    return min(delay, max_delay)


def is_captcha_error(error_message: str) -> bool:
    """判断错误是否为验证码相关错误
    
    Args:
        error_message: 错误信息
        
    Returns:
        是否为验证码错误
    """
    if not error_message:
        return False
    
    error_message = error_message.lower()
    captcha_keywords = [
        '验证码', 'captcha', 'verification code', 
        '图形验证码', '验证码错误', 'captcha error'
    ]
    
    return any(keyword in error_message for keyword in captcha_keywords)


def extract_cookies_from_response(response_headers: Dict[str, str]) -> Dict[str, str]:
    """从响应头中提取Cookie
    
    Args:
        response_headers: 响应头字典
        
    Returns:
        Cookie字典
    """
    cookies = {}
    
    # 查找Set-Cookie头
    set_cookie_header = None
    for key, value in response_headers.items():
        if key.lower() == 'set-cookie':
            set_cookie_header = value
            break
    
    if not set_cookie_header:
        return cookies
    
    # 解析Cookie
    try:
        # 简单的Cookie解析，实际项目中可能需要更复杂的解析逻辑
        cookie_pairs = set_cookie_header.split(';')
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
    except Exception as e:
        logger.warning(f"解析Cookie失败: {str(e)}")
    
    return cookies


def build_request_headers(user_agent: str = None, referer: str = None, 
                         additional_headers: Dict[str, str] = None) -> Dict[str, str]:
    """构建请求头
    
    Args:
        user_agent: User-Agent
        referer: Referer
        additional_headers: 额外的请求头
        
    Returns:
        请求头字典
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    if user_agent:
        headers['User-Agent'] = user_agent
    else:
        headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/91.0.4472.124 Safari/537.36')
    
    if referer:
        headers['Referer'] = referer
    
    if additional_headers:
        headers.update(additional_headers)
    
    return headers