# -*- coding: utf-8 -*-

"""
外部平台客户端
封装与外部平台的HTTP交互
"""

import logging
import requests
from typing import Dict, Optional, Tuple, Any
from urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)


class ExternalPlatformClient:
    """外部平台HTTP客户端"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """初始化客户端
        
        Args:
            base_url: 平台基础URL
            timeout: 请求超时时间
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logger.info(f"ExternalPlatformClient初始化 - base_url: {self.base_url}")

    def get_captcha(self, captcha_endpoint: str = '/captcha') -> Tuple[Optional[bytes], Optional[Dict]]:
        """获取验证码图片和初始Cookie
        
        Args:
            captcha_endpoint: 验证码端点路径
            
        Returns:
            (验证码图片字节数据, Cookie字典)
        """
        url = urljoin(self.base_url, captcha_endpoint)
        logger.info(f"获取验证码 - URL: {url}")
        
        start_time = time.time()
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # 获取响应时间
            response_time = int((time.time() - start_time) * 1000)
            
            # 提取Cookie
            cookies = dict(response.cookies)
            
            logger.info(f"验证码获取成功 - 响应时间: {response_time}ms, "
                       f"图片大小: {len(response.content)} bytes, "
                       f"Cookie数量: {len(cookies)}")
            
            return response.content, cookies
            
        except requests.RequestException as e:
            response_time = int((time.time() - start_time) * 1000)
            logger.error(f"获取验证码失败 - URL: {url}, 响应时间: {response_time}ms, "
                        f"错误: {str(e)}", exc_info=True)
            return None, None

    def login(self, login_endpoint: str, username: str, password: str, 
              captcha: str, cookies: Optional[Dict] = None, 
              additional_data: Optional[Dict] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """执行登录操作
        
        Args:
            login_endpoint: 登录端点路径
            username: 用户名
            password: 密码
            captcha: 验证码
            cookies: Cookie字典
            additional_data: 额外的登录数据
            
        Returns:
            (登录是否成功, 响应Cookie字典, 错误信息)
        """
        url = urljoin(self.base_url, login_endpoint)
        logger.info(f"开始登录 - URL: {url}, 用户名: {username}")
        
        # 准备登录数据
        login_data = {
            'act':'login',
            'name': username,
            'password': password,
            'login_code': captcha,
            'login_user_no': '0000',
            'ck_autologin': ''
        }
        
        if additional_data:
            login_data.update(additional_data)
        
        # 设置Cookie
        if cookies:
            self.session.cookies.update(cookies)
        
        start_time = time.time()
        try:
            response = self.session.post(
                url, 
                data=login_data, 
                timeout=self.timeout,
                allow_redirects=False  # 不自动跟随重定向
            )
            
            response_time = int((time.time() - start_time) * 1000)
            
            # 获取响应Cookie
            response_cookies = dict(response.cookies)
            
            # 判断登录是否成功
            # 通常成功登录会返回302重定向或特定的响应内容
            success = self._check_login_success(response)
            
            if success:
                logger.info(f"登录成功 - 用户名: {username}, 响应时间: {response_time}ms, "
                           f"状态码: {response.status_code}")
                return True, response_cookies, None
            else:
                error_msg = self._extract_error_message(response)
                logger.warning(f"登录失败 - 用户名: {username}, 响应时间: {response_time}ms, "
                              f"状态码: {response.status_code}, 错误: {error_msg}")
                return False, response_cookies, error_msg
                
        except requests.RequestException as e:
            response_time = int((time.time() - start_time) * 1000)
            error_msg = f"登录请求失败: {str(e)}"
            logger.error(f"登录请求异常 - 用户名: {username}, 响应时间: {response_time}ms, "
                        f"错误: {error_msg}", exc_info=True)
            return False, None, error_msg

    def check_login_status(self, check_endpoint: str = '/user/info', 
                          cookies: Optional[Dict] = None) -> Tuple[bool, Optional[str]]:
        """检查登录状态
        
        Args:
            check_endpoint: 状态检查端点
            cookies: Cookie字典
            
        Returns:
            (是否已登录, 错误信息)
        """
        url = urljoin(self.base_url, check_endpoint)
        logger.debug(f"检查登录状态 - URL: {url}")
        
        # 设置Cookie
        if cookies:
            self.session.cookies.update(cookies)
        
        start_time = time.time()
        try:
            response = self.session.get(url, timeout=self.timeout)
            response_time = int((time.time() - start_time) * 1000)
            
            # 判断是否已登录
            is_logged_in = self._check_login_status_response(response)
            
            if is_logged_in:
                logger.debug(f"登录状态检查 - 已登录, 响应时间: {response_time}ms")
                return True, None
            else:
                error_msg = "未登录或会话已过期"
                logger.debug(f"登录状态检查 - {error_msg}, 响应时间: {response_time}ms")
                return False, error_msg
                
        except requests.RequestException as e:
            response_time = int((time.time() - start_time) * 1000)
            error_msg = f"状态检查请求失败: {str(e)}"
            logger.error(f"登录状态检查异常 - 响应时间: {response_time}ms, "
                        f"错误: {error_msg}", exc_info=True)
            return False, error_msg

    def make_authenticated_request(self, method: str, endpoint: str, 
                                 cookies: Optional[Dict] = None,
                                 data: Optional[Dict] = None,
                                 params: Optional[Dict] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """发送认证请求
        
        Args:
            method: HTTP方法
            endpoint: 端点路径
            cookies: Cookie字典
            data: POST数据
            params: URL参数
            
        Returns:
            (请求是否成功, 响应数据, 错误信息)
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"发送认证请求 - {method} {url}")
        
        # 设置Cookie
        if cookies:
            self.session.cookies.update(cookies)
        
        start_time = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                data=data,
                params=params,
                timeout=self.timeout
            )
            
            response_time = int((time.time() - start_time) * 1000)
            response.raise_for_status()
            
            try:
                response_data = response.json()
            except ValueError:
                response_data = {'content': response.text}
            
            logger.debug(f"认证请求成功 - {method} {url}, 响应时间: {response_time}ms")
            return True, response_data, None
            
        except requests.RequestException as e:
            response_time = int((time.time() - start_time) * 1000)
            error_msg = f"认证请求失败: {str(e)}"
            logger.error(f"认证请求异常 - {method} {url}, 响应时间: {response_time}ms, "
                        f"错误: {error_msg}", exc_info=True)
            return False, None, error_msg

    def _check_login_success(self, response: requests.Response) -> bool:
        """检查登录响应是否表示成功
        
        Args:
            response: HTTP响应对象
            
        Returns:
            是否登录成功
        """
        # 302重定向通常表示登录成功
        if response.status_code == 302:
            return True
        
        # 200状态码需要检查响应内容
        if response.status_code == 200:
            try:
                data = response.json()
                # 根据实际API响应格式调整
                # {
                #     "status": "success",
                #     "des": "登录成功",
                #     "res": {
                #         "code": 0
                #     }
                # }
                return data.get('status') == 'success' or data.get('des') == '登录成功'
            except ValueError:
                # 非JSON响应，检查是否包含成功标识
                content = response.text.lower()
                return 'success' in content or '成功' in content
        
        return False

    def _check_login_status_response(self, response: requests.Response) -> bool:
        """检查状态检查响应是否表示已登录
        
        Args:
            response: HTTP响应对象
            
        Returns:
            是否已登录
        """
        if response.status_code != 200:
            return False
        
        try:
            data = response.json()
            # 根据实际API响应格式调整
            return data.get('authenticated', False) or 'user' in data
        except ValueError:
            # 非JSON响应，检查是否包含用户信息
            content = response.text.lower()
            return 'user' in content and 'login' not in content

    def _extract_error_message(self, response: requests.Response) -> str:
        """从响应中提取错误信息
        
        Args:
            response: HTTP响应对象
            
        Returns:
            错误信息
        """
        try:
            data = response.json()
            return data.get('message', data.get('error', '未知错误'))
        except ValueError:
            # 非JSON响应，返回状态码
            return f"HTTP {response.status_code}"

    def execute_complete_login_flow(self, task_id: str, platform, platform_config: Dict) -> Dict[str, Any]:
        """执行完整的登录流程（包含业务日志记录和会话管理）
        
        Args:
            task_id: 任务ID
            platform: 平台对象
            platform_config: 平台配置字典
            
        Returns:
            登录结果字典，包含：
            - success: 是否成功
            - session_id: 会话ID（成功时）
            - platform_sign: 平台标识
            - account: 账户名
            - expire_time: 过期时间
            - error: 错误信息（如果失败）
        """

        # 从配置中获取登录凭据
        login_config = platform_config.get('login_config')
        if not login_config:
            error_msg = "平台登录配置不存在"
            logger.error(f"登录配置验证失败 - 平台: {platform.sign}, 错误: {error_msg}")
            return {'success': False, 'error': error_msg}
        
        # 确保 login_config 是字典类型
        if isinstance(login_config, str):
            try:
                import json
                login_config = json.loads(login_config)
            except json.JSONDecodeError:
                error_msg = "登录配置格式错误，无法解析JSON"
                logger.error(f"登录配置解析失败 - 平台: {platform.sign}, 错误: {error_msg}")
                return {'success': False, 'error': error_msg}
        
        account = login_config.get('account') if isinstance(login_config, dict) else None
        password = login_config.get('password') if isinstance(login_config, dict) else None
        
        # 验证必要的登录配置
        if not account or not password:
            error_msg = "平台登录配置不完整：缺少账户名或密码"
            logger.error(f"登录配置验证失败 - 平台: {platform.sign}, 账户: {account}, 错误: {error_msg}")
            return {'success': False, 'error': error_msg}

        logger.info(f"开始登录流程 - 任务ID: {task_id}, 平台: {platform.sign}, 账户: {account}")
        
        try:
            # 步骤1: 获取验证码
            captcha_endpoint = platform_config['endpoints']['captcha']
            captcha_image, initial_cookies = self.get_captcha(captcha_endpoint)
            
            if not captcha_image or not initial_cookies:
                error_msg = "获取验证码失败"
                # 记录失败日志
                from external_platform.services.request_log import log_request_failure
                log_request_failure(platform, account, captcha_endpoint, error_msg)
                return {'success': False, 'error': error_msg}
            
            logger.info(f"验证码获取成功 - 任务ID: {task_id}, 图片大小: {len(captcha_image)} bytes")
            
            # 步骤2: 获取验证码服务并识别验证码
            from common.captcha_service import get_captcha_service
            captcha_service = get_captcha_service()
            if not captcha_service:
                error_msg = "验证码服务不可用"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            captcha_type = platform_config.get('captcha_type', 1004)
            captcha_result = captcha_service.recognize_captcha(captcha_image, captcha_type)
            
            if captcha_result.get('err_no') != 0:
                error_msg = f"验证码识别失败: {captcha_result.get('err_str', '未知错误')}"
                logger.error(f"验证码识别失败 - 任务ID: {task_id}, 错误: {error_msg}")
                return {'success': False, 'error': error_msg}
            
            captcha_text = captcha_result.get('pic_str', '')
            pic_id = captcha_result.get('pic_id', '')
            
            logger.info(f"验证码识别成功 - 任务ID: {task_id}, 识别结果: {captcha_text}, pic_id: {pic_id}")
            
            # 步骤3: 执行登录
            login_endpoint = platform_config['endpoints']['login']
            additional_data = platform_config.get('login_data_extra', {})
            
            success, response_cookies, error_msg = self.login(
                login_endpoint, account, password, captcha_text, 
                initial_cookies, additional_data
            )
            
            if not success:
                # 如果是验证码错误且有pic_id，报告给超级鹰
                if pic_id and ('验证码' in error_msg or 'captcha' in error_msg.lower()):
                    captcha_service.report_error(pic_id)
                    logger.info(f"已报告验证码错误 - pic_id: {pic_id}")
                
                return {'success': False, 'error': error_msg}
            
            # 步骤4: 记录成功日志
            from external_platform.services.request_log import (
                log_captcha_request, log_captcha_recognition, log_login_request
            )
            
            # 记录验证码识别日志
            request_log = log_captcha_request(platform, account, captcha_endpoint, captcha_result)
            if request_log:
                log_captcha_recognition(request_log, captcha_result)
            
            # 合并Cookie
            all_cookies = {**initial_cookies, **response_cookies} if response_cookies else initial_cookies
            
            # 记录登录请求日志
            log_login_request(platform, account, login_endpoint, True, None, all_cookies)
            
            # 步骤5: 保存认证会话
            from django.utils import timezone
            from external_platform.services.auth_service import AuthService
            
            auth_data = {
                'cookies': all_cookies,
                'login_time': timezone.now().isoformat(),
                'task_id': task_id
            }
            
            session_timeout = platform_config.get('session_timeout_hours', 24)
            session = AuthService.create_or_update_session(
                platform.sign, account, auth_data, session_timeout
            )
            
            if not session:
                error_msg = "保存认证会话失败"
                logger.error(f"保存会话失败 - 任务ID: {task_id}")
                return {'success': False, 'error': error_msg}
            
            logger.info(f"登录流程完成 - 任务ID: {task_id}, 会话ID: {session.id}")
            
            return {
                'success': True,
                'session_id': session.id,
                'platform_sign': platform.sign,
                'account': account,
                'expire_time': session.expire_time.isoformat() if session.expire_time else None
            }
            
        except Exception as e:
            error_msg = f"登录流程异常: {str(e)}"
            logger.error(f"完整登录流程异常 - 任务ID: {task_id}, 账户: {account}, 错误: {error_msg}", exc_info=True)
            return {'success': False, 'error': error_msg}

    def close(self):
        """关闭客户端会话"""
        if self.session:
            self.session.close()
            logger.debug("ExternalPlatformClient会话已关闭")