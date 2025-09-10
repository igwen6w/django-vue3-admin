# -*- coding: utf-8 -*-

"""
平台网关SDK配置管理模块
负责从Django settings加载和验证网关配置
"""

import logging
import os
from typing import Dict, Any, Optional
from django.conf import settings

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class GatewayConfig:
    """网关配置管理类
    
    负责加载、验证和管理网关相关的配置项
    """
    
    # 必需的配置字段
    REQUIRED_FIELDS = [
        'USERNAME',
        'PASSWORD', 
        'BASE_URL',
        'CAPTCHA_BASE_URL'
    ]
    
    # 配置字段默认值
    DEFAULT_VALUES = {
        'LOGIN_URL': '/login',
        'CAPTCHA_TYPE': 1004,  # 超级鹰英数字混合验证码类型
        'CAPTCHA_MAX_RETRIES': 3,
        'KEEPALIVE_INTERVAL': 300,  # 5分钟
        'SESSION_TIMEOUT': 3600,    # 1小时
        'MAX_RETRIES': 3,
        'REDIS_KEY_PREFIX': 'gateway:',
        'REQUEST_TIMEOUT': 30,      # 请求超时时间
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    def __init__(self):
        """初始化配置管理器"""
        self._config = None
        self._chaojiying_config = None
        self._load_config()
        logger.info("网关配置管理器初始化完成")
    
    def _load_config(self) -> None:
        """从Django settings加载配置"""
        try:
            # 加载主配置
            gateway_settings = getattr(settings, 'GATEWAY_SETTINGS', {})
            if not gateway_settings:
                raise ConfigurationError(
                    "GATEWAY_SETTINGS配置未找到，请在Django settings中配置",
                    config_section='GATEWAY_SETTINGS'
                )
            
            # 验证必需字段
            self._validate_required_fields(gateway_settings)
            
            # 合并默认配置
            self._config = self._merge_with_defaults(gateway_settings)
            
            # 加载超级鹰配置
            self._load_chaojiying_config()
            
            # 验证配置有效性
            self._validate_config()
            
            logger.info("网关配置加载成功")
            
        except Exception as e:
            logger.error(f"配置加载失败: {e}")
            if not isinstance(e, ConfigurationError):
                raise ConfigurationError(f"配置加载异常: {e}")
            raise
    
    def _validate_required_fields(self, config: Dict[str, Any]) -> None:
        """验证必需的配置字段"""
        missing_fields = []
        
        for field in self.REQUIRED_FIELDS:
            value = config.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
        
        if missing_fields:
            raise ConfigurationError(
                f"缺少必需的配置字段: {', '.join(missing_fields)}",
                config_section='GATEWAY_SETTINGS',
                details={'missing_fields': missing_fields}
            )
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """合并用户配置和默认配置"""
        merged_config = {}
        
        # 转换配置键名并设置值
        for key, value in config.items():
            # 转换为小写下划线格式
            config_key = key.lower()
            merged_config[config_key] = value
        
        # 设置默认值
        for key, default_value in self.DEFAULT_VALUES.items():
            config_key = key.lower()
            if config_key not in merged_config:
                merged_config[config_key] = default_value
        
        return merged_config
    
    def _load_chaojiying_config(self) -> None:
        """加载超级鹰验证码服务配置"""
        chaojiying_config = getattr(settings, 'CHAOJIYING_CONFIG', {})
        
        if not chaojiying_config:
            logger.warning("CHAOJIYING_CONFIG配置未找到，验证码功能可能不可用")
            self._chaojiying_config = {}
            return
        
        # 验证超级鹰配置
        required_chaojiying_fields = ['username', 'password', 'software_id']
        missing_fields = [
            field for field in required_chaojiying_fields 
            if not chaojiying_config.get(field)
        ]
        
        if missing_fields:
            raise ConfigurationError(
                f"超级鹰配置不完整，缺少字段: {', '.join(missing_fields)}",
                config_section='CHAOJIYING_CONFIG',
                details={'missing_fields': missing_fields}
            )
        
        self._chaojiying_config = chaojiying_config
        logger.info("超级鹰配置加载成功")
    
    def _validate_config(self) -> None:
        """验证配置的有效性"""
        # 验证URL格式
        base_url = self.get('base_url')
        if not base_url.startswith(('http://', 'https://')):
            raise ConfigurationError(
                "BASE_URL必须以http://或https://开头",
                config_key='BASE_URL'
            )
        
        captcha_base_url = self.get('captcha_base_url')
        if not captcha_base_url.startswith(('http://', 'https://')):
            raise ConfigurationError(
                "CAPTCHA_BASE_URL必须以http://或https://开头",
                config_key='CAPTCHA_BASE_URL'
            )
        
        # 验证数值类型配置
        numeric_configs = [
            ('captcha_type', 'CAPTCHA_TYPE'),
            ('captcha_max_retries', 'CAPTCHA_MAX_RETRIES'), 
            ('keepalive_interval', 'KEEPALIVE_INTERVAL'),
            ('session_timeout', 'SESSION_TIMEOUT'),
            ('max_retries', 'MAX_RETRIES'),
            ('request_timeout', 'REQUEST_TIMEOUT'),
        ]
        
        for config_key, original_key in numeric_configs:
            value = self.get(config_key)
            if not isinstance(value, int) or value <= 0:
                raise ConfigurationError(
                    f"{original_key}必须是正整数",
                    config_key=original_key
                )
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项
        
        Args:
            key: 配置键名（小写下划线格式）
            default: 默认值
            
        Returns:
            配置值
        """
        if self._config is None:
            raise ConfigurationError("配置尚未加载")
        
        return self._config.get(key, default)
    
    def get_chaojiying_config(self) -> Dict[str, Any]:
        """获取超级鹰配置
        
        Returns:
            超级鹰配置字典
        """
        if self._chaojiying_config is None:
            raise ConfigurationError("超级鹰配置尚未加载")
        
        return self._chaojiying_config.copy()
    
    def is_chaojiying_available(self) -> bool:
        """检查超级鹰服务是否可用
        
        Returns:
            是否可用
        """
        return bool(self._chaojiying_config)
    
    def get_redis_key(self, suffix: str) -> str:
        """生成Redis键名
        
        Args:
            suffix: 键名后缀
            
        Returns:
            完整的Redis键名
        """
        prefix = self.get('redis_key_prefix', 'gateway:')
        return f"{prefix}{suffix}"
    
    def get_captcha_url(self) -> str:
        """构建验证码URL（不含时间戳参数）
        
        Returns:
            验证码基础URL
        """
        return self.get('captcha_base_url')
    
    def get_login_url(self) -> str:
        """获取完整的登录URL
        
        Returns:
            完整的登录URL
        """
        base_url = self.get('base_url').rstrip('/')
        login_path = self.get('login_url')
        
        if login_path.startswith('/'):
            return f"{base_url}{login_path}"
        else:
            return f"{base_url}/{login_path}"
    
    def get_request_headers(self) -> Dict[str, str]:
        """获取请求头配置
        
        Returns:
            请求头字典
        """
        return {
            'User-Agent': self.get('user_agent'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """导出配置为字典（隐藏敏感信息）
        
        Returns:
            配置字典
        """
        if self._config is None:
            return {}
        
        # 复制配置并隐藏敏感信息
        config_copy = self._config.copy()
        
        # 隐藏敏感字段
        sensitive_fields = ['username', 'password']
        for field in sensitive_fields:
            if field in config_copy:
                config_copy[field] = '*' * 8
        
        return config_copy
    
    def reload(self) -> None:
        """重新加载配置"""
        logger.info("重新加载网关配置")
        self._config = None
        self._chaojiying_config = None
        self._load_config()


# 全局配置实例
_config_instance = None


def get_gateway_config() -> GatewayConfig:
    """获取全局网关配置实例
    
    Returns:
        GatewayConfig实例
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = GatewayConfig()
    
    return _config_instance


def reload_gateway_config() -> None:
    """重新加载全局配置"""
    global _config_instance
    
    if _config_instance is not None:
        _config_instance.reload()
    else:
        _config_instance = GatewayConfig()


# 便捷函数
def get_config(key: str, default: Any = None) -> Any:
    """获取配置项的便捷函数
    
    Args:
        key: 配置键名
        default: 默认值
        
    Returns:
        配置值
    """
    return get_gateway_config().get(key, default)


def get_chaojiying_config() -> Dict[str, Any]:
    """获取超级鹰配置的便捷函数
    
    Returns:
        超级鹰配置字典
    """
    return get_gateway_config().get_chaojiying_config()


def is_chaojiying_available() -> bool:
    """检查超级鹰服务是否可用的便捷函数
    
    Returns:
        是否可用
    """
    return get_gateway_config().is_chaojiying_available()