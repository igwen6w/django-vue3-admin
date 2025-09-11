# -*- coding: utf-8 -*-

"""
平台网关SDK会话管理器
负责会话生命周期管理的核心组件，包括登录、验证码处理、会话存储等
"""

import json
import time
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import requests
import redis
from django.utils import timezone

from .config import get_gateway_config, get_chaojiying_config, is_chaojiying_available
from .exceptions import (
    GatewayError, AuthenticationError, SessionExpiredError, 
    PlatformUnavailableError, CaptchaError, PlatformAPIError, ConfigurationError
)
from .utils import (
    serialize_cookies, deserialize_cookies, build_url_with_timestamp,
    validate_response, extract_error_message, create_session_with_config,
    log_request_info, mask_sensitive_info, retry_with_backoff
)

logger = logging.getLogger(__name__)


class SessionManager:
    """会话管理器核心类
    
    负责管理与外部平台的会话，包括：
    - 登录认证和验证码处理
    - 会话持久化存储（Redis）
    - 请求拦截和自动重试
    - 会话过期检测和刷新
    """
    
    def __init__(self, redis_client: Optional[redis.Redis] = None, 
                 config: Optional[Dict[str, Any]] = None):
        """初始化会话管理器
        
        Args:
            redis_client: Redis客户端实例，如果为None则使用默认连接
            config: 配置字典，如果为None则使用全局配置
        """
        # 加载配置
        self.config = config or get_gateway_config()
        
        # 初始化Redis客户端
        self.redis_client = redis_client or self._create_redis_client()
        
        # 创建requests会话
        self.session = self._create_http_session()
        
        # 会话状态
        self._session_data = {}
        self._last_activity_time = None
        self._login_attempts = 0
        self._max_login_attempts = 3
        
        # 超级鹰验证码服务
        self._captcha_service = None
        self._initialize_captcha_service()
        
        logger.info("SessionManager初始化完成")
    
    def _create_redis_client(self) -> redis.Redis:
        """创建Redis客户端"""
        try:
            # 从Django settings获取Redis配置
            from django.conf import settings
            
            redis_config = getattr(settings, 'CACHES', {}).get('default', {})
            if redis_config.get('BACKEND') == 'django_redis.cache.RedisCache':
                # 使用Django Redis缓存配置
                redis_url = redis_config.get('LOCATION', 'redis://127.0.0.1:6379/1')
            else:
                # 使用默认配置
                redis_url = 'redis://127.0.0.1:6379/1'
            
            # 使用Redis.from_url()方法创建客户端，自动处理URL解析
            client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # 测试连接
            client.ping()
            logger.info(f"Redis连接成功: {redis_url}")
            return client
            
        except Exception as e:
            # 提供详细的错误信息用于调试
            try:
                from django.conf import settings
                redis_config = getattr(settings, 'CACHES', {}).get('default', {})
                redis_url = redis_config.get('LOCATION', 'redis://127.0.0.1:6379/1')
                logger.error(f"Redis连接失败: {e}")
                logger.error(f"Redis配置URL: {redis_url}")
            except:
                logger.error(f"Redis连接失败: {e}")
            raise ConfigurationError(f"Redis连接失败: {e}")
    
    def _create_http_session(self) -> requests.Session:
        """创建HTTP会话"""
        try:
            config_dict = self.config.to_dict() if hasattr(self.config, 'to_dict') else {}
            # logger.warning(f"config_dict: {config_dict}")
            session = create_session_with_config(config_dict)
            
            # 设置超时
            timeout = self.config.get('request_timeout', 30)
            session.timeout = timeout
            
            logger.info("HTTP会话创建成功")
            return session
            
        except Exception as e:
            logger.error(f"HTTP会话创建失败: {e}")
            raise ConfigurationError(f"HTTP会话创建失败: {e}")
    
    def _initialize_captcha_service(self) -> None:
        """初始化验证码服务"""
        try:
            if not is_chaojiying_available():
                logger.warning("超级鹰验证码服务不可用，验证码功能将被禁用")
                return
            
            from common.captcha_service import get_captcha_service
            self._captcha_service = get_captcha_service()
            
            if self._captcha_service:
                logger.info("超级鹰验证码服务初始化成功")
            else:
                logger.warning("超级鹰验证码服务初始化失败")
                
        except ImportError as e:
            logger.error(f"验证码服务模块导入失败: {e}")
            raise ConfigurationError(f"验证码服务不可用: {e}")
        except Exception as e:
            logger.error(f"验证码服务初始化异常: {e}")
            self._captcha_service = None
    
    def _build_captcha_url(self) -> str:
        """构建验证码URL，包含随机时间戳参数
        
        Returns:
            带时间戳的验证码URL
        """
        base_url = self.config.get('captcha_base_url')
        if not base_url:
            raise ConfigurationError("CAPTCHA_BASE_URL配置未设置")
        
        captcha_url = build_url_with_timestamp(base_url, 't')
        logger.debug(f"构建验证码URL: {captcha_url}")
        return captcha_url
    
    def _get_captcha_image(self, captcha_url: str) -> Tuple[bytes, Dict[str, str]]:
        """从固定链接获取验证码图片和Cookie
        
        Args:
            captcha_url: 验证码URL
            
        Returns:
            (验证码图片字节数据, Cookie字典)
        """
        start_time = time.time()
        
        try:
            response = self.session.get(captcha_url, timeout=30)
            response.raise_for_status()
            
            image_data = response.content
            cookies = response.cookies.get_dict()
            
            duration = time.time() - start_time
            
            logger.info(f"验证码获取成功 - 图片大小: {len(image_data)} bytes, "
                       f"Cookie数量: {len(cookies)}, 耗时: {duration:.2f}s")
            
            log_request_info('GET', captcha_url, response, duration)
            
            return image_data, cookies
            
        except requests.RequestException as e:
            duration = time.time() - start_time
            error_msg = f"获取验证码失败: {e}"
            logger.error(f"{error_msg}, 耗时: {duration:.2f}s")
            
            log_request_info('GET', captcha_url, None, duration, error=str(e))
            raise CaptchaError(error_msg, details={'url': captcha_url, 'duration': duration})
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"验证码获取异常: {e}"
            logger.error(f"{error_msg}, 耗时: {duration:.2f}s")
            raise CaptchaError(error_msg, details={'url': captcha_url, 'duration': duration})
    
    def _solve_captcha(self, image_data: bytes) -> str:
        """调用captcha_service识别验证码
        
        Args:
            image_data: 验证码图片字节数据
            
        Returns:
            识别出的验证码文本
        """
        if not self._captcha_service:
            raise CaptchaError("验证码服务不可用，请检查超级鹰配置")
        
        captcha_type = self.config.get('captcha_type', 1004)
        max_retries = self.config.get('captcha_max_retries', 3)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"开始第{attempt + 1}次验证码识别尝试，类型: {captcha_type}")
                
                result = self._captcha_service.recognize_captcha(image_data, captcha_type)
                
                if result.get('err_no') == 0:
                    captcha_text = result.get('pic_str', '')
                    pic_id = result.get('pic_id', '')
                    
                    logger.info(f"验证码识别成功 - 结果: {captcha_text}, pic_id: {pic_id}")
                    return captcha_text
                else:
                    error_msg = result.get('err_str', '未知错误')
                    last_error = CaptchaError(
                        f"验证码识别失败: {error_msg}",
                        pic_id=result.get('pic_id'),
                        captcha_type=captcha_type,
                        retry_count=attempt + 1
                    )
                    
                    logger.warning(f"验证码识别失败 - 第{attempt + 1}次尝试, 错误: {error_msg}")
                    
                    if attempt == max_retries - 1:
                        raise last_error
                        
            except CaptchaError:
                raise
            except Exception as e:
                last_error = CaptchaError(
                    f"验证码识别异常: {e}",
                    captcha_type=captcha_type,
                    retry_count=attempt + 1
                )
                
                logger.error(f"验证码识别异常 - 第{attempt + 1}次尝试, 错误: {e}")
                
                if attempt == max_retries - 1:
                    raise last_error
        
        # 理论上不会到达这里
        raise last_error or CaptchaError("验证码识别重试次数已用完")
    
    def _check_login_success(self, response: requests.Response) -> bool:
        """检查登录响应是否表示成功
        
        Args:
            response: HTTP响应对象
            
        Returns:
            是否登录成功
        """
        try:
            # 302重定向通常表示登录成功
            if response.status_code == 302:
                logger.info("检测到302重定向，登录可能成功")
                return True
            
            # 200状态码需要检查响应内容
            if response.status_code == 200:
                try:
                    # 尝试解析JSON响应
                    if 'application/json' in response.headers.get('content-type', '').lower():
                        data = response.json()
                        
                        # 常见的成功标识
                        success_indicators = [
                            data.get('status') == 'success',
                            data.get('success') is True,
                            data.get('code') == 0,
                            data.get('code') == '0',
                            '成功' in str(data.get('message', '')),
                            '成功' in str(data.get('msg', '')),
                        ]
                        
                        if any(success_indicators):
                            logger.info("JSON响应表示登录成功")
                            return True
                            
                except (ValueError, json.JSONDecodeError):
                    pass
                
                # 检查HTML响应中的成功标识
                content = response.text.lower()
                success_keywords = ['success', '成功', '登录成功', 'welcome', '欢迎']
                failure_keywords = ['error', '错误', '失败', '验证码', 'captcha', 'login']
                
                success_count = sum(1 for keyword in success_keywords if keyword in content)
                failure_count = sum(1 for keyword in failure_keywords if keyword in content)
                
                if success_count > failure_count:
                    logger.info("HTML内容表示登录成功")
                    return True
            
            logger.warning(f"登录响应未表示成功: HTTP {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"检查登录结果时发生异常: {e}")
            return False
    
    def get_redis_key(self, suffix: str) -> str:
        """生成Redis键名
        
        Args:
            suffix: 键名后缀
            
        Returns:
            完整的Redis键名
        """
        prefix = self.config.get('redis_key_prefix', 'gateway:')
        return f"{prefix}{suffix}"
    
    def is_session_valid(self) -> bool:
        """检查会话是否有效
        
        通过以下步骤验证会话：
        1. 检查内存和Redis中的会话数据
        2. 检查会话过期时间
        3. 检查Cookie是否存在
        4. 发送实际HTTP请求验证Cookie有效性
        
        Returns:
            会话是否有效
        """
        logger.debug(f"检查会话是否有效: {self._session_data}")
        try:
            # 检查内存中的会话数据
            if not self._session_data:
                self._load_session_from_redis()
            
            if not self._session_data:
                logger.debug("会话数据为空")
                return False
            
            # 检查过期时间
            expires_at_str = self._session_data.get('expires_at')
            if expires_at_str:
                try:
                    expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                    if timezone.now() > expires_at:
                        logger.info("会话已过期")
                        return False
                except (ValueError, TypeError) as e:
                    logger.warning(f"解析会话过期时间失败: {e}")
            
            # 检查Cookie是否存在
            cookies = self._session_data.get('cookies', {})
            if not cookies:
                logger.debug("会话Cookie为空")
                return False
            
            # 通过实际HTTP请求验证Cookie有效性
            if not self._validate_session_with_request():
                logger.info("HTTP请求验证显示会话已失效")
                return False
            
            logger.debug("会话验证通过")
            return True
            
        except Exception as e:
            logger.error(f"会话有效性检查异常: {e}")
            return False
    
    def _load_session_from_redis(self) -> None:
        """从Redis加载会话数据"""
        try:
            session_key = self.get_redis_key('session:main')
            session_data_str = self.redis_client.get(session_key)
            
            if session_data_str:
                self._session_data = json.loads(session_data_str)
                
                # 更新最后访问时间
                self._last_activity_time = time.time()
                
                logger.debug("会话数据从Redis加载成功")
            else:
                self._session_data = {}
                logger.debug("Redis中没有找到会话数据")
                
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"从Redis加载会话数据失败: {e}")
            self._session_data = {}
        except Exception as e:
            logger.error(f"加载会话数据时发生异常: {e}")
            self._session_data = {}
    
    def _validate_session_with_request(self) -> bool:
        """通过实际HTTP请求验证会话有效性
        
        发送请求到 main.php 页面，检查响应内容：
        - 如果响应是 <script>top.location.href='./';</script> 表示cookie已失效
        - 其他响应表示cookie仍然有效
        
        Returns:
            bool: cookie是否有效
        """
        try:

            # 构建完整URL
            full_url = self._build_full_url('/main.php')

            logger.debug(f"发送请求验证会话有效性: {full_url}")
                
            # 执行请求
            response = self._execute_request('GET', full_url, allow_redirects=False)
            
            # 检查响应内容
            response_text = response.text.strip()

            logger.debug(f"响应内容: {response_text}")
            
            # 检查是否是会话失效的标识响应
            session_expired_indicator = "<script>top.location.href='./';</script>"
            
            if response_text == session_expired_indicator:
                logger.info("检测到会话失效响应，cookie已过期")
                return False
            
            # 检查HTTP状态码
            # if response.status_code == 401:
            #     logger.info("HTTP 401响应，会话未授权")
            #     return False
            
            # 检查是否有其他重定向到登录页面的迹象
            # if response.status_code in [302, 303, 307, 308]:
            #     location = response.headers.get('Location', '')
            #     if 'login' in location.lower() or location.endswith('./'):
            #         logger.info(f"重定向到登录页面: {location}")
            #         return False
            
            logger.debug("HTTP请求验证通过，会话仍然有效")
            return True
            
        except requests.RequestException as e:
            logger.warning(f"验证会话的HTTP请求失败: {e}")
            # 网络请求失败时，我们不能确定会话状态，保守地返回True
            # 避免因为网络问题导致频繁重新登录
            return True
        except Exception as e:
            logger.error(f"验证会话时发生异常: {e}")
            return True
    
    def close(self) -> None:
        """关闭会话管理器，清理资源"""
        try:
            if self.session:
                self.session.close()
                logger.debug("HTTP会话已关闭")
            
            if self.redis_client:
                self.redis_client.close()
                logger.debug("Redis连接已关闭")
                
        except Exception as e:
            logger.error(f"关闭会话管理器时发生异常: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    def get_session_info(self) -> Dict[str, Any]:
        """获取会话信息（隐藏敏感数据）
        
        Returns:
            会话信息字典
        """
        try:
            if not self._session_data:
                self._load_session_from_redis()
            
            info = {}
            
            if self._session_data:
                info.update({
                    'created_at': self._session_data.get('created_at'),
                    'last_accessed': self._session_data.get('last_accessed'),
                    'expires_at': self._session_data.get('expires_at'),
                    'login_info': self._session_data.get('login_info', {}),
                    'cookies_count': len(self._session_data.get('cookies', {})),
                    'is_valid': self.is_session_valid()
                })
            
            info.update({
                'last_activity_time': self._last_activity_time,
                'login_attempts': self._login_attempts,
                'captcha_service_available': self._captcha_service is not None
            })
            
            return info
            
        except Exception as e:
            logger.error(f"获取会话信息失败: {e}")
            return {'error': str(e)}
    
    def login(self) -> bool:
        """执行完整的登录流程
        
        根据设计文档，登录流程为：
        1. 从固定验证码链接获取验证码图片和Cookie
        2. 调用captcha_service识别验证码
        3. 使用识别结果和Cookie提交登录
        4. 保存会话到Redis
        
        Returns:
            登录是否成功
        """
        start_time = time.time()
        
        try:
            logger.info("开始执行登录流程")
            
            # 检查登录尝试次数
            if self._login_attempts >= self._max_login_attempts:
                raise AuthenticationError(
                    f"登录尝试次数超限（{self._max_login_attempts}次）",
                    details={'attempts': self._login_attempts}
                )
            
            self._login_attempts += 1
            
            # 步骤1: 获取验证码图片和Cookie
            captcha_url = self._build_captcha_url()
            image_data, initial_cookies = self._get_captcha_image(captcha_url)
            
            # 步骤2: 识别验证码
            captcha_text = self._solve_captcha(image_data)
            
            # 步骤3: 执行登录
            login_success, response_cookies = self._perform_login(captcha_text, initial_cookies)
            
            if not login_success:
                logger.warning(f"登录失败 - 第{self._login_attempts}次尝试")
                return False
            
            # 步骤4: 保存会话到Redis
            all_cookies = {**initial_cookies, **(response_cookies or {})}
            self._save_session_to_redis(all_cookies, {
                'captcha_url': captcha_url,
                'login_time': timezone.now().isoformat(),
                'captcha_text': mask_sensitive_info(captcha_text)
            })
            
            # 重置登录尝试次数
            self._login_attempts = 0
            
            duration = time.time() - start_time
            logger.info(f"登录成功，总耗时: {duration:.2f}s")
            
            return True
            
        except (CaptchaError, AuthenticationError, PlatformUnavailableError):
            # 这些异常直接重新抛出
            raise
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"登录流程异常: {e}"
            logger.error(f"{error_msg}，耗时: {duration:.2f}s")
            raise GatewayError(error_msg, details={'duration': duration, 'attempts': self._login_attempts})
    
    def _perform_login(self, captcha_text: str, cookies: Dict[str, str]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """执行登录请求
        
        Args:
            captcha_text: 验证码文本
            cookies: 初始 Cookie字典
            
        Returns:
            (登录是否成功, 响应Cookie字典)
        """
        start_time = time.time()
        
        try:
            # 更新session的cookies
            self.session.cookies.update(cookies)
            
            # 准备登录数据
            login_data = {
                'act': 'login',
                'name': self.config.get('username'),
                'password': self.config.get('password'),
                'login_code': captcha_text,
                'login_user_no': '0000',
                'ck_autologin': ''
            }
            
            # 获取登录URL
            login_url = self.config.get_login_url() if hasattr(self.config, 'get_login_url') else \
                       f"{self.config.get('base_url').rstrip('/')}{self.config.get('login_url', '/login')}"
            
            logger.info(f"提交登录请求 - 用户: {mask_sensitive_info(login_data['name'])}")
            
            # 执行登录请求
            response = self.session.post(
                login_url,
                data=login_data,
                allow_redirects=False,  # 不自动跟随重定向
                timeout=self.config.get('request_timeout', 30)
            )
            
            duration = time.time() - start_time
            
            # 获取响应Cookie
            response_cookies = response.cookies.get_dict()
            
            # 判断登录是否成功
            success = self._check_login_success(response)
            
            log_request_info('POST', login_url, response, duration, 
                           success=success, cookies_count=len(response_cookies))
            
            if not success:
                error_msg = extract_error_message(response)
                logger.warning(f"登录失败 - 响应: {error_msg}")
                
                # 如果是验证码错误，可能需要报告给超级鹰
                if '验证码' in error_msg or 'captcha' in error_msg.lower():
                    logger.info("检测到验证码错误，可能需要报告给超级鹰")
                
                return False, response_cookies
            
            logger.info(f"登录请求成功，耗时: {duration:.2f}s")
            return True, response_cookies
            
        except requests.RequestException as e:
            duration = time.time() - start_time
            error_msg = f"登录请求失败: {e}"
            logger.error(f"{error_msg}，耗时: {duration:.2f}s")
            
            log_request_info('POST', login_url, None, duration, error=str(e))
            raise PlatformUnavailableError(error_msg, platform_url=login_url)
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"登录请求异常: {e}"
            logger.error(f"{error_msg}，耗时: {duration:.2f}s")
            raise GatewayError(error_msg, details={'duration': duration})
    
    def _save_session_to_redis(self, cookies: Dict[str, str], login_info: Dict[str, Any]) -> None:
        """保存会话数据到Redis
        
        Args:
            cookies: Cookie字典
            login_info: 登录信息
        """
        try:
            now = timezone.now()
            session_timeout = self.config.get('session_timeout', 3600)  # 默认1小时
            expires_at = now + timedelta(seconds=session_timeout)
            
            # 构建会话数据
            session_data = {
                'cookies': cookies,
                'headers': {
                    'X-CSRFToken': cookies.get('csrftoken', ''),
                    # 可以根据需要添加其他header
                },
                'created_at': now.isoformat(),
                'last_accessed': now.isoformat(),
                'expires_at': expires_at.isoformat(),
                'login_info': login_info
            }
            
            # 保存到Redis
            session_key = self.get_redis_key('session:main')
            session_data_str = json.dumps(session_data, ensure_ascii=False)
            
            # 设置过期时间（比会话过期时间稍长一些）
            redis_ttl = session_timeout + 300  # 额外5分钟缓冲
            
            self.redis_client.setex(session_key, redis_ttl, session_data_str)
            
            # 更新内存中的会话数据
            self._session_data = session_data
            self._last_activity_time = time.time()
            
            # 更新HTTP会话的cookies
            self.session.cookies.update(cookies)
            
            logger.info(f"会话数据已保存到Redis - 过期时间: {expires_at.isoformat()}, "
                       f"Cookie数量: {len(cookies)}")
            
        except redis.RedisError as e:
            error_msg = f"Redis保存会话失败: {e}"
            logger.error(error_msg)
            raise GatewayError(error_msg)
        except Exception as e:
            error_msg = f"保存会话数据异常: {e}"
            logger.error(error_msg)
            raise GatewayError(error_msg)
    
    def save_session(self, cookies: Dict[str, str]) -> None:
        """公开的保存会话方法
        
        Args:
            cookies: Cookie字典
        """
        login_info = {
            'manual_save': True,
            'save_time': timezone.now().isoformat()
        }
        self._save_session_to_redis(cookies, login_info)
    
    def load_session(self) -> Dict[str, Any]:
        """公开的加载会话方法
        
        Returns:
            会话数据字典
        """
        self._load_session_from_redis()
        return self._session_data.copy() if self._session_data else {}
    
    def clear_session(self) -> None:
        """清除会话数据"""
        try:
            # 清除Redis中的数据
            session_key = self.get_redis_key('session:main')
            self.redis_client.delete(session_key)
            
            # 清除内存中的数据
            self._session_data = {}
            self._last_activity_time = None
            
            # 清除HTTP会话的cookies
            self.session.cookies.clear()
            
            logger.info("会话数据已清除")
            
        except redis.RedisError as e:
            logger.error(f"Redis清除会话失败: {e}")
        except Exception as e:
            logger.error(f"清除会话数据异常: {e}")
    
    def refresh_session(self) -> bool:
        """刷新过期会话
        
        Returns:
            刷新是否成功
        """
        try:
            logger.info("开始刷新会话")
            
            # 清除旧会话
            self.clear_session()
            
            # 重新登录
            return self.login()
            
        except Exception as e:
            logger.error(f"刷新会话失败: {e}")
            return False
    
    def refresh(self) -> bool:
        """刷新过期会话（别名方法）
        
        Returns:
            刷新是否成功
        """
        return self.refresh_session()
    
    def update_session_activity(self) -> None:
        """更新会话活动时间"""
        try:
            if not self._session_data:
                return
            
            now = timezone.now()
            self._session_data['last_accessed'] = now.isoformat()
            self._last_activity_time = time.time()
            
            # 更新Redis中的数据
            session_key = self.get_redis_key('session:main')
            session_data_str = json.dumps(self._session_data, ensure_ascii=False)
            
            # 保持原有的TTL
            ttl = self.redis_client.ttl(session_key)
            if ttl > 0:
                self.redis_client.setex(session_key, ttl, session_data_str)
            
            logger.debug("会话活动时间已更新")
            
        except Exception as e:
            logger.error(f"更新会话活动时间失败: {e}")
    
    def extend_session(self, extra_seconds: int = 3600) -> bool:
        """延长会话有效期
        
        Args:
            extra_seconds: 额外的秒数
            
        Returns:
            延长是否成功
        """
        try:
            if not self._session_data:
                logger.warning("没有活跃会话，无法延长")
                return False
            
            # 更新过期时间
            current_expires = self._session_data.get('expires_at')
            if current_expires:
                try:
                    expires_at = datetime.fromisoformat(current_expires.replace('Z', '+00:00'))
                    new_expires_at = expires_at + timedelta(seconds=extra_seconds)
                    self._session_data['expires_at'] = new_expires_at.isoformat()
                    
                    # 更新Redis
                    session_key = self.get_redis_key('session:main')
                    session_data_str = json.dumps(self._session_data, ensure_ascii=False)
                    
                    # 计算新的TTL
                    new_ttl = int((new_expires_at - timezone.now()).total_seconds()) + 300
                    self.redis_client.setex(session_key, max(new_ttl, 60), session_data_str)
                    
                    logger.info(f"会话已延长{extra_seconds}秒，新过期时间: {new_expires_at.isoformat()}")
                    return True
                    
                except (ValueError, TypeError) as e:
                    logger.error(f"解析过期时间失败: {e}")
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"延长会话失败: {e}")
            return False
    
    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """核心请求方法，自动处理认证和会话过期
        
        Args:
            method: HTTP方法
            path: API路径
            **kwargs: 其他requests参数
            
        Returns:
            HTTP响应对象
        """
        start_time = time.time()
        max_retries = self.config.get('max_retries', 3)
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # 检查和准备会话
                if not self._prepare_session_for_request():
                    raise SessionExpiredError("会话无效且刷新失败")
                
                # 构建完整URL
                full_url = self._build_full_url(path)
                
                # 执行请求
                response = self._execute_request(method, full_url, **kwargs)
                
                # 检查响应是否表示会话过期
                if self._is_session_expired_response(response):
                    logger.warning(f"检测到会话过期响应 - 第{attempt + 1}次尝试")
                    
                    if attempt < max_retries:
                        # 尝试刷新会话
                        if self.refresh_session():
                            continue
                        else:
                            raise SessionExpiredError("会话过期且刷新失败")
                    else:
                        raise SessionExpiredError("会话过期且重试次数超限")
                
                # 请求成功，更新活动时间
                self.update_session_activity()
                
                duration = time.time() - start_time
                log_request_info(method, full_url, response, duration, attempt=attempt + 1)
                
                return response
                
            except (SessionExpiredError, AuthenticationError):
                # 这些异常需要特殊处理
                raise
            except (requests.RequestException, PlatformUnavailableError) as e:
                last_exception = e
                
                if attempt < max_retries:
                    # 计算重试延迟
                    from .exceptions import calculate_retry_delay
                    delay = calculate_retry_delay(e, attempt + 1)
                    
                    logger.warning(f"请求失败，{delay}秒后重试 - 第{attempt + 1}次尝试: {e}")
                    
                    if delay > 0:
                        time.sleep(delay)
                    continue
                else:
                    logger.error(f"请求失败，重试{max_retries}次后放弃: {e}")
                    raise PlatformUnavailableError(f"请求失败: {e}", platform_url=full_url)
            except Exception as e:
                last_exception = e
                logger.error(f"请求异常 - 第{attempt + 1}次尝试: {e}")
                
                if attempt == max_retries:
                    duration = time.time() - start_time
                    raise GatewayError(f"请求异常: {e}", details={
                        'method': method,
                        'path': path,
                        'attempts': attempt + 1,
                        'duration': duration
                    })
        
        # 理论上不会到达这里
        raise last_exception or GatewayError("请求失败")
    
    def _prepare_session_for_request(self) -> bool:
        """为请求准备会话
        
        Returns:
            会话是否准备就绪
        """
        try:
            # 检查会话是否有效
            if self.is_session_valid():
                return True
            
            logger.warning("会话无效，尝试登录")
            
            # 尝试登录
            if self.login():
                return True
            
            logger.error("登录失败，无法准备会话")
            return False
            
        except Exception as e:
            logger.error(f"准备会话异常: {e}")
            return False
    
    def _build_full_url(self, path: str) -> str:
        """构建完整的URL
        
        Args:
            path: API路径
            
        Returns:
            完整的URL
        """
        base_url = self.config.get('base_url', '').rstrip('/')
        
        if path.startswith('http'):
            # 已经是完整URL
            return path
        elif path.startswith('/'):
            # 绝对路径
            return f"{base_url}{path}"
        else:
            # 相对路径
            return f"{base_url}/{path}"
    
    def _execute_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """执行具体的HTTP请求
        
        Args:
            method: HTTP方法
            url: 完整URL
            **kwargs: requests参数
            
        Returns:
            HTTP响应对象
        """
        try:
            # 设置默认超时
            if 'timeout' not in kwargs:
                kwargs['timeout'] = self.config.get('request_timeout', 30)
            
            # 执行请求
            response = self.session.request(method, url, **kwargs)
            
            # 检查HTTP状态码
            if response.status_code >= 500:
                raise PlatformUnavailableError(
                    f"服务器错误: HTTP {response.status_code}",
                    platform_url=url,
                    status_code=response.status_code
                )
            elif response.status_code >= 400:
                error_msg = extract_error_message(response)
                raise PlatformAPIError(
                    f"API调用失败: {url} {error_msg}",
                    status_code=response.status_code,
                    api_endpoint=url,
                    response_data=self._safe_get_response_data(response)
                )
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"HTTP请求异常: {e}")
            raise PlatformUnavailableError(f"HTTP请求异常: {e}", platform_url=url)
    
    def _is_session_expired_response(self, response: requests.Response) -> bool:
        """检查响应是否表示会话过期
        
        Args:
            response: HTTP响应对象
            
        Returns:
            是否会话过期
        """
        try:
            # 检查状态码
            if response.status_code == 401:
                return True
            
            # 检查响应内容
            if response.status_code == 200:
                try:
                    if 'application/json' in response.headers.get('content-type', '').lower():
                        data = response.json()
                        
                        # 常见的会话过期标识
                        expired_indicators = [
                            data.get('code') == 401,
                            data.get('status') == 'unauthorized',
                            '未登录' in str(data.get('message', '')),
                            '会话过期' in str(data.get('message', '')),
                            'session expired' in str(data.get('message', '')).lower(),
                        ]
                        
                        if any(expired_indicators):
                            return True
                            
                except (ValueError, json.JSONDecodeError):
                    pass
                
                # 检查HTML响应
                content = response.text.lower()
                expired_keywords = ['未登录', '会话过期', 'login', 'unauthorized']
                
                if any(keyword in content for keyword in expired_keywords):
                    return True
            
            # 检查重定向到登录页面
            if response.status_code == 302:
                location = response.headers.get('location', '').lower()
                if 'login' in location:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"检查会话过期响应异常: {e}")
            return False
    
    def _safe_get_response_data(self, response: requests.Response) -> Optional[Dict]:
        """安全获取响应数据
        
        Args:
            response: HTTP响应对象
            
        Returns:
            响应数据或None
        """
        try:
            if 'application/json' in response.headers.get('content-type', '').lower():
                return response.json()
        except (ValueError, json.JSONDecodeError):
            pass
        
        return None