# -*- coding: utf-8 -*-

"""
外部平台客户端
封装与外部平台的HTTP交互
"""

import logging
import requests
from typing import Dict, Optional, Tuple
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
            'username': username,
            'password': password,
            'captcha': captcha
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
                return data.get('success', False) or data.get('code') == 0
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

    def close(self):
        """关闭客户端会话"""
        if self.session:
            self.session.close()
            logger.debug("ExternalPlatformClient会话已关闭")