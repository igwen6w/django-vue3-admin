# -*- coding: utf-8 -*-

"""
平台网关SDK通用工具函数
提供Cookie序列化、时间戳生成、响应处理等通用功能
"""

import json
import time
import random
import logging
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from requests.cookies import RequestsCookieJar

from .exceptions import GatewayError

logger = logging.getLogger(__name__)


def serialize_cookies(cookies: Union[Dict, RequestsCookieJar]) -> str:
    """序列化Cookie字典为JSON字符串
    
    Args:
        cookies: Cookie字典或RequestsCookieJar对象
        
    Returns:
        JSON字符串
    """
    try:
        if isinstance(cookies, RequestsCookieJar):
            # 转换RequestsCookieJar为字典
            cookie_dict = {}
            for cookie in cookies:
                cookie_dict[cookie.name] = cookie.value
            cookies = cookie_dict
        elif not isinstance(cookies, dict):
            logger.warning(f"Cookie类型不支持: {type(cookies)}")
            return '{}'
        
        return json.dumps(cookies, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Cookie序列化失败: {e}")
        return '{}'


def deserialize_cookies(cookies_str: str) -> Dict[str, str]:
    """反序列化JSON字符串为Cookie字典
    
    Args:
        cookies_str: JSON字符串
        
    Returns:
        Cookie字典
    """
    try:
        if not cookies_str or not cookies_str.strip():
            return {}
        
        cookies = json.loads(cookies_str)
        if not isinstance(cookies, dict):
            logger.warning(f"反序列化的Cookie不是字典类型: {type(cookies)}")
            return {}
        
        # 确保所有值都是字符串
        return {str(k): str(v) for k, v in cookies.items()}
    except json.JSONDecodeError as e:
        logger.error(f"Cookie反序列化JSON解析失败: {e}")
        return {}
    except Exception as e:
        logger.error(f"Cookie反序列化失败: {e}")
        return {}


def generate_timestamp() -> int:
    """生成带随机数的时间戳，用于防止缓存
    
    Returns:
        时间戳（毫秒级别 + 随机数）
    """
    # 当前时间戳(毫秒) + 4位随机数
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    return timestamp + random_suffix


def build_url_with_timestamp(base_url: str, param_name: str = 't') -> str:
    """为URL添加时间戳参数防止缓存
    
    Args:
        base_url: 基础URL
        param_name: 时间戳参数名
        
    Returns:
        带时间戳参数的URL
    """
    try:
        # 解析URL
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        
        # 添加时间戳参数
        timestamp = generate_timestamp()
        query_params[param_name] = [str(timestamp)]
        
        # 重建URL
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        
        return urlunparse(new_parsed)
    except Exception as e:
        logger.error(f"构建带时间戳URL失败: {e}")
        # 降级处理：简单拼接
        separator = '&' if '?' in base_url else '?'
        timestamp = generate_timestamp()
        return f"{base_url}{separator}{param_name}={timestamp}"


def validate_response(response: requests.Response) -> bool:
    """验证HTTP响应是否成功
    
    Args:
        response: HTTP响应对象
        
    Returns:
        是否成功（2xx状态码）
    """
    if not isinstance(response, requests.Response):
        return False
    
    return 200 <= response.status_code < 300


def extract_error_message(response: requests.Response) -> str:
    """从HTTP响应中提取错误信息
    
    Args:
        response: HTTP响应对象
        
    Returns:
        错误信息字符串
    """
    try:
        # 尝试解析JSON响应
        if hasattr(response, 'json'):
            try:
                data = response.json()
                
                # 常见的错误字段名
                error_fields = ['message', 'error', 'msg', 'error_message', 'detail']
                for field in error_fields:
                    if field in data and data[field]:
                        return str(data[field])
                
                # 如果没有找到错误字段，返回整个响应
                if isinstance(data, dict) and len(data) == 1:
                    return str(list(data.values())[0])
                    
            except (ValueError, json.JSONDecodeError):
                pass
        
        # 尝试从响应文本中提取错误信息
        if hasattr(response, 'text') and response.text:
            text = response.text.strip()
            if len(text) < 500:  # 只有较短的文本才可能是错误信息
                return text
        
        # 默认返回HTTP状态码
        return f"HTTP {response.status_code}"
        
    except Exception as e:
        logger.error(f"提取错误信息失败: {e}")
        return f"HTTP {getattr(response, 'status_code', 'Unknown')}"


def safe_get_config(config: Optional[Dict], key: str, default: Any = None) -> Any:
    """安全获取配置项
    
    Args:
        config: 配置字典
        key: 配置键名
        default: 默认值
        
    Returns:
        配置值
    """
    if not config or not isinstance(config, dict):
        return default
    
    return config.get(key, default)


def format_duration(seconds: float) -> str:
    """格式化时间间隔为可读字符串
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m{secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h{minutes}m"


def mask_sensitive_info(text: str, mask_char: str = '*') -> str:
    """遮盖敏感信息
    
    Args:
        text: 原始文本
        mask_char: 遮盖字符
        
    Returns:
        遮盖后的文本
    """
    if not text or len(text) <= 4:
        return mask_char * len(text) if text else ''
    
    # 保留前2位和后2位
    prefix = text[:2]
    suffix = text[-2:]
    middle = mask_char * (len(text) - 4)
    
    return f"{prefix}{middle}{suffix}"


def create_session_with_config(config: Dict[str, Any]) -> requests.Session:
    """根据配置创建requests会话
    
    Args:
        config: 配置字典
        
    Returns:
        配置好的requests.Session对象
    """
    session = requests.Session()
    
    # 设置请求头
    headers = {
        'User-Agent': safe_get_config(
            config, 'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    session.headers.update(headers)
    
    # 设置超时
    timeout = safe_get_config(config, 'request_timeout', 30)
    session.timeout = timeout
    
    return session


def log_request_info(method: str, url: str, response: requests.Response = None, 
                    duration: float = None, **kwargs) -> None:
    """记录请求信息日志
    
    Args:
        method: HTTP方法
        url: 请求URL
        response: 响应对象
        duration: 请求耗时
        **kwargs: 其他信息
    """
    try:
        # 遮盖URL中的敏感信息
        safe_url = mask_url_sensitive_info(url)
        
        # 构建日志信息
        log_parts = [f"{method} {safe_url}"]
        
        if response:
            log_parts.append(f"status={response.status_code}")
        
        if duration is not None:
            log_parts.append(f"duration={format_duration(duration)}")
        
        # 添加其他信息
        for key, value in kwargs.items():
            if value is not None:
                log_parts.append(f"{key}={value}")
        
        log_message = " ".join(log_parts)
        
        # 根据响应状态选择日志级别
        if response and response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)
            
    except Exception as e:
        logger.error(f"记录请求日志失败: {e}")


def mask_url_sensitive_info(url: str) -> str:
    """遮盖URL中的敏感信息
    
    Args:
        url: 原始URL
        
    Returns:
        遮盖敏感信息后的URL
    """
    try:
        parsed = urlparse(url)
        
        # 遮盖密码
        if parsed.password:
            netloc = parsed.netloc.replace(f":{parsed.password}@", ":***@")
            parsed = parsed._replace(netloc=netloc)
        
        # 遮盖查询参数中的敏感信息
        if parsed.query:
            query_params = parse_qs(parsed.query)
            sensitive_params = ['password', 'token', 'key', 'secret', 'auth']
            
            for param in sensitive_params:
                if param in query_params:
                    query_params[param] = ['***']
            
            new_query = urlencode(query_params, doseq=True)
            parsed = parsed._replace(query=new_query)
        
        return urlunparse(parsed)
    except Exception:
        # 如果解析失败，只显示域名部分
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}/***"
        except Exception:
            return "***"


def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0, 
                      backoff_factor: float = 2.0, max_delay: float = 60.0, 
                      exceptions: tuple = (Exception,)) -> Any:
    """带指数退避的重试装饰器
    
    Args:
        func: 要重试的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟时间
        backoff_factor: 退避因子
        max_delay: 最大延迟时间
        exceptions: 需要重试的异常类型
        
    Returns:
        函数执行结果
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                
                if attempt == max_retries:
                    logger.error(f"函数{func.__name__}重试{max_retries}次后仍然失败: {e}")
                    raise
                
                # 计算延迟时间
                delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                logger.warning(f"函数{func.__name__}第{attempt + 1}次尝试失败，{delay}秒后重试: {e}")
                
                time.sleep(delay)
        
        # 理论上不会到达这里
        raise last_exception
    
    return wrapper


def chunk_list(lst: list, chunk_size: int) -> list:
    """将列表分块
    
    Args:
        lst: 原始列表
        chunk_size: 块大小
        
    Returns:
        分块后的列表
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size必须大于0")
    
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def deep_merge_dict(dict1: Dict, dict2: Dict) -> Dict:
    """深度合并两个字典
    
    Args:
        dict1: 字典1
        dict2: 字典2
        
    Returns:
        合并后的字典
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    
    return result


def is_json_response(response: requests.Response) -> bool:
    """判断响应是否为JSON格式
    
    Args:
        response: HTTP响应对象
        
    Returns:
        是否为JSON格式
    """
    try:
        content_type = response.headers.get('content-type', '').lower()
        return 'application/json' in content_type or 'text/json' in content_type
    except Exception:
        return False


def safe_json_parse(text: str, default: Any = None) -> Any:
    """安全解析JSON字符串
    
    Args:
        text: JSON字符串
        default: 解析失败时的默认值
        
    Returns:
        解析结果或默认值
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default