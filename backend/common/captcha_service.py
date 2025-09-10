# -*- coding: utf-8 -*-

"""
验证码识别服务
集成超级鹰平台API进行验证码识别
"""

import logging
import requests
from hashlib import md5
from typing import Dict, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class CaptchaService:
    """超级鹰验证码服务客户端，用于处理验证码识别相关操作"""
    
    def __init__(self, username: str, password: str, software_id: str):
        """初始化验证码客户端
        
        Args:
            username: 超级鹰平台用户名
            password: 超级鹰平台密码
            software_id: 超级鹰平台软件ID
        """
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.software_id = software_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.software_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        logger.info(f"CaptchaService初始化成功 - 用户: {self.username}")

    def recognize_captcha(self, image_data: bytes, captcha_type: int) -> Dict:
        """提交图片进行验证码识别
        
        Args:
            image_data: 图片字节数据
            captcha_type: 验证码类型，参考http://www.chaojiying.com/price.html
            
        Returns:
            识别结果JSON数据
            成功: {'err_no': 0, 'pic_id': '123456', 'pic_str': 'abcd', 'md5': '...'}
            失败: {'err_no': 错误码, 'err_str': '错误描述'}
        """
        logger.info(f"开始识别验证码 - 类型: {captcha_type}, 图片大小: {len(image_data)} bytes")
        
        params = {'codetype': captcha_type}
        params.update(self.base_params)
        files = {'userfile': ('captcha.jpg', image_data)}
        
        try:
            response = requests.post(
                'http://upload.chaojiying.net/Upload/Processing.php',
                data=params,
                files=files,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('err_no') == 0:
                logger.info(f"验证码识别成功 - pic_id: {result.get('pic_id')}, "
                           f"识别结果: {result.get('pic_str')}")
            else:
                logger.warning(f"验证码识别失败 - 错误码: {result.get('err_no')}, "
                              f"错误信息: {result.get('err_str')}")
            
            return result
            
        except requests.RequestException as e:
            error_msg = f"验证码识别请求失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'err_no': -1, 'err_str': error_msg}
        except Exception as e:
            error_msg = f"验证码识别异常: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'err_no': -2, 'err_str': error_msg}

    def report_error(self, pic_id: str) -> Dict:
        """报告识别错误，用于退分
        
        Args:
            pic_id: 图片ID
            
        Returns:
            操作结果
        """
        logger.info(f"报告验证码识别错误 - pic_id: {pic_id}")
        
        params = {'id': pic_id}
        params.update(self.base_params)
        
        try:
            response = requests.post(
                'http://upload.chaojiying.net/Upload/ReportError.php',
                data=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('err_no') == 0:
                logger.info(f"验证码错误报告成功 - pic_id: {pic_id}")
            else:
                logger.warning(f"验证码错误报告失败 - pic_id: {pic_id}, "
                              f"错误: {result.get('err_str')}")
            
            return result
            
        except requests.RequestException as e:
            error_msg = f"报告验证码错误请求失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'err_no': -1, 'err_str': error_msg}

    def get_balance(self) -> Dict:
        """查询账户余额
        
        Returns:
            余额信息
        """
        logger.debug("查询超级鹰账户余额")
        
        try:
            response = requests.post(
                'http://upload.chaojiying.net/Upload/GetScore.php',
                data=self.base_params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('err_no') == 0:
                logger.info(f"账户余额查询成功 - 余额: {result.get('tifen')}")
            else:
                logger.warning(f"账户余额查询失败 - 错误: {result.get('err_str')}")
            
            return result
            
        except requests.RequestException as e:
            error_msg = f"查询余额请求失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'err_no': -1, 'err_str': error_msg}


def get_captcha_service() -> Optional[CaptchaService]:
    """获取验证码服务实例
    
    Returns:
        CaptchaService实例，如果配置不完整则返回None
    """
    try:
        config = getattr(settings, 'CHAOJIYING_CONFIG', {})
        username = config.get('username')
        password = config.get('password')
        software_id = config.get('software_id')
        
        if not all([username, password, software_id]):
            logger.error("超级鹰配置不完整，无法创建CaptchaService实例")
            return None
            
        return CaptchaService(username, password, software_id)
        
    except Exception as e:
        logger.error(f"创建CaptchaService实例失败: {str(e)}", exc_info=True)
        return None