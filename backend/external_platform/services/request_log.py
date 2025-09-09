# -*- coding: utf-8 -*-

"""
请求日志服务
统一处理外部平台请求的日志记录
"""

import logging
from typing import Dict, Optional, Any
from django.utils import timezone

from external_platform.models import Platform, RequestLog, ExternalAuthCaptchaLog, PlatformEndpoint, AuthSession
from external_platform.choices import ApiMethod

logger = logging.getLogger(__name__)


class RequestLogService:
    """请求日志服务类"""
    
    @staticmethod
    def log_request_failure(platform: Platform, account: str, endpoint_path: str, 
                           error_msg: str, response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录请求失败日志
        
        Args:
            platform: 平台对象
            account: 账户名
            endpoint_path: 端点路径
            error_msg: 错误信息
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            # 尝试获取对应的平台端点配置
            platform_endpoint = RequestLogService._get_platform_endpoint_by_path(
                platform, endpoint_path
            )
            
            log_record = RequestLog.objects.create(
                platform=platform,
                platform_endpoint=platform_endpoint,
                account=account,
                endpoint_path=endpoint_path,
                method=ApiMethod.GET,
                status_code=500,
                error_message=error_msg,
                response_time_ms=response_time_ms,
                tag={'type': 'request_failure', 'timestamp': timezone.now().isoformat()}
            )
            
            logger.debug(f"记录请求失败日志成功 - 平台: {platform.sign}, 账户: {account}, "
                        f"端点: {endpoint_path}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录请求失败日志异常 - 平台: {platform.sign}, 账户: {account}, "
                        f"端点: {endpoint_path}, 错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_captcha_request(platform: Platform, account: str, endpoint_path: str, 
                           captcha_result: Dict, response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录验证码请求日志
        
        Args:
            platform: 平台对象
            account: 账户名
            endpoint_path: 端点路径
            captcha_result: 验证码识别结果
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            platform_endpoint = RequestLogService._get_platform_endpoint_by_type(
                platform, 'captcha'
            )
            
            is_success = captcha_result.get('err_no') == 0
            
            log_record = RequestLog.objects.create(
                platform=platform,
                platform_endpoint=platform_endpoint,
                account=account,
                endpoint_path=endpoint_path,
                method=ApiMethod.GET,
                status_code=200 if is_success else 400,
                response_time_ms=response_time_ms,
                response_body=captcha_result,
                tag={
                    'type': 'captcha_request', 
                    'success': is_success,
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            logger.debug(f"记录验证码请求日志成功 - 平台: {platform.sign}, 账户: {account}, "
                        f"成功: {is_success}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录验证码请求日志异常 - 平台: {platform.sign}, 账户: {account}, "
                        f"错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_captcha_recognition(request_log: RequestLog, captcha_result: Dict) -> Optional[ExternalAuthCaptchaLog]:
        """记录验证码识别结果
        
        Args:
            request_log: 请求日志对象
            captcha_result: 验证码识别结果
            
        Returns:
            创建的验证码日志对象
        """
        try:
            captcha_log = ExternalAuthCaptchaLog.objects.create(
                request_log=request_log,
                # 可以根据需要添加更多验证码识别相关的字段
            )
            
            logger.debug(f"记录验证码识别日志成功 - 请求日志ID: {request_log.id}, "
                        f"验证码日志ID: {captcha_log.id}")
            return captcha_log
            
        except Exception as e:
            logger.error(f"记录验证码识别日志异常 - 请求日志ID: {request_log.id}, "
                        f"错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_login_request(platform: Platform, account: str, endpoint_path: str, 
                         success: bool, error_msg: Optional[str], 
                         response_cookies: Optional[Dict], 
                         response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录登录请求日志
        
        Args:
            platform: 平台对象
            account: 账户名
            endpoint_path: 端点路径
            success: 是否成功
            error_msg: 错误信息
            response_cookies: 响应Cookie
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            platform_endpoint = RequestLogService._get_platform_endpoint_by_type(
                platform, 'login'
            )
            
            log_record = RequestLog.objects.create(
                platform=platform,
                platform_endpoint=platform_endpoint,
                account=account,
                endpoint_path=endpoint_path,
                method=ApiMethod.POST,
                status_code=200 if success else 400,
                response_body={'cookies': response_cookies} if response_cookies else None,
                error_message=error_msg if not success else None,
                response_time_ms=response_time_ms,
                tag={
                    'type': 'login_request', 
                    'success': success,
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            logger.debug(f"记录登录请求日志成功 - 平台: {platform.sign}, 账户: {account}, "
                        f"成功: {success}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录登录请求日志异常 - 平台: {platform.sign}, 账户: {account}, "
                        f"错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_status_check_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                                success: bool, response_data: Optional[Dict], 
                                error_msg: Optional[str], 
                                response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录状态检查请求日志
        
        Args:
            session: 认证会话对象
            platform_endpoint: 平台端点对象
            success: 是否成功
            response_data: 响应数据
            error_msg: 错误信息
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            log_record = RequestLog.objects.create(
                platform=session.platform,
                platform_endpoint=platform_endpoint,
                account=session.account,
                endpoint_path=platform_endpoint.path,
                method=platform_endpoint.http_method,
                status_code=200 if success else 400,
                response_body=response_data,
                error_message=error_msg if not success else None,
                response_time_ms=response_time_ms,
                tag={
                    'type': 'status_check', 
                    'success': success, 
                    'session_id': session.id,
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            logger.debug(f"记录状态检查请求日志成功 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 成功: {success}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录状态检查请求日志异常 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_workorder_list_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                                  success: bool, response_data: Optional[Dict], 
                                  error_msg: Optional[str], payload: Dict,
                                  response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录工单列表请求日志
        
        Args:
            session: 认证会话对象
            platform_endpoint: 平台端点对象
            success: 是否成功
            response_data: 响应数据
            error_msg: 错误信息
            payload: 请求载荷
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            log_record = RequestLog.objects.create(
                platform=session.platform,
                platform_endpoint=platform_endpoint,
                account=session.account,
                endpoint_path=platform_endpoint.path,
                method=platform_endpoint.http_method,
                payload=payload,
                status_code=200 if success else 400,
                response_body=response_data,
                error_message=error_msg if not success else None,
                response_time_ms=response_time_ms,
                tag={
                    'type': 'workorder_list', 
                    'success': success, 
                    'session_id': session.id,
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            logger.debug(f"记录工单列表请求日志成功 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 成功: {success}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录工单列表请求日志异常 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def log_workorder_detail_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                                   success: bool, response_data: Optional[Dict], 
                                   error_msg: Optional[str], payload: Dict,
                                   response_time_ms: int = 0) -> Optional[RequestLog]:
        """记录工单详情请求日志
        
        Args:
            session: 认证会话对象
            platform_endpoint: 平台端点对象
            success: 是否成功
            response_data: 响应数据
            error_msg: 错误信息
            payload: 请求载荷
            response_time_ms: 响应时间（毫秒）
            
        Returns:
            创建的日志记录对象
        """
        try:
            log_record = RequestLog.objects.create(
                platform=session.platform,
                platform_endpoint=platform_endpoint,
                account=session.account,
                endpoint_path=platform_endpoint.path,
                method=platform_endpoint.http_method,
                payload=payload,
                status_code=200 if success else 400,
                response_body=response_data,
                error_message=error_msg if not success else None,
                response_time_ms=response_time_ms,
                tag={
                    'type': 'workorder_detail', 
                    'success': success, 
                    'session_id': session.id,
                    'timestamp': timezone.now().isoformat()
                }
            )
            
            logger.debug(f"记录工单详情请求日志成功 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 成功: {success}, 日志ID: {log_record.id}")
            return log_record
            
        except Exception as e:
            logger.error(f"记录工单详情请求日志异常 - 平台: {session.platform.sign}, "
                        f"账户: {session.account}, 错误: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def _get_platform_endpoint_by_path(platform: Platform, endpoint_path: str) -> Optional[PlatformEndpoint]:
        """根据端点路径获取平台端点配置
        
        Args:
            platform: 平台对象
            endpoint_path: 端点路径
            
        Returns:
            平台端点对象
        """
        try:
            # 根据endpoint_path推断端点类型
            endpoint_type = None
            if 'captcha' in endpoint_path.lower():
                endpoint_type = 'captcha'
            elif 'login' in endpoint_path.lower():
                endpoint_type = 'login'
            elif 'workorder' in endpoint_path.lower():
                if 'list' in endpoint_path.lower():
                    endpoint_type = 'workorder_list'
                elif 'detail' in endpoint_path.lower():
                    endpoint_type = 'workorder_detail'
            elif 'status' in endpoint_path.lower() or 'check' in endpoint_path.lower():
                endpoint_type = 'check_status'
            
            if endpoint_type:
                return PlatformEndpoint.objects.get(
                    platform=platform, 
                    endpoint_type=endpoint_type
                )
        except PlatformEndpoint.DoesNotExist:
            logger.debug(f"未找到平台端点配置 - 平台: {platform.sign}, "
                        f"端点路径: {endpoint_path}")
        except Exception as e:
            logger.error(f"获取平台端点配置异常 - 平台: {platform.sign}, "
                        f"端点路径: {endpoint_path}, 错误: {str(e)}")
        
        return None

    @staticmethod
    def _get_platform_endpoint_by_type(platform: Platform, endpoint_type: str) -> Optional[PlatformEndpoint]:
        """根据端点类型获取平台端点配置
        
        Args:
            platform: 平台对象
            endpoint_type: 端点类型
            
        Returns:
            平台端点对象
        """
        try:
            return PlatformEndpoint.objects.get(
                platform=platform, 
                endpoint_type=endpoint_type
            )
        except PlatformEndpoint.DoesNotExist:
            logger.debug(f"未找到平台端点配置 - 平台: {platform.sign}, "
                        f"端点类型: {endpoint_type}")
        except Exception as e:
            logger.error(f"获取平台端点配置异常 - 平台: {platform.sign}, "
                        f"端点类型: {endpoint_type}, 错误: {str(e)}")
        
        return None


# 便捷的函数接口，保持向后兼容
def log_request_failure(platform: Platform, account: str, endpoint_path: str, 
                       error_msg: str, response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录请求失败日志（便捷函数）"""
    return RequestLogService.log_request_failure(
        platform, account, endpoint_path, error_msg, response_time_ms
    )


def log_captcha_request(platform: Platform, account: str, endpoint_path: str, 
                       captcha_result: Dict, response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录验证码请求日志（便捷函数）"""
    return RequestLogService.log_captcha_request(
        platform, account, endpoint_path, captcha_result, response_time_ms
    )


def log_captcha_recognition(request_log: RequestLog, captcha_result: Dict) -> Optional[ExternalAuthCaptchaLog]:
    """记录验证码识别结果（便捷函数）"""
    return RequestLogService.log_captcha_recognition(request_log, captcha_result)


def log_login_request(platform: Platform, account: str, endpoint_path: str, 
                     success: bool, error_msg: Optional[str], 
                     response_cookies: Optional[Dict], 
                     response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录登录请求日志（便捷函数）"""
    return RequestLogService.log_login_request(
        platform, account, endpoint_path, success, error_msg, 
        response_cookies, response_time_ms
    )


def log_status_check_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                           success: bool, response_data: Optional[Dict], 
                           error_msg: Optional[str], 
                           response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录状态检查请求日志（便捷函数）"""
    return RequestLogService.log_status_check_request(
        session, platform_endpoint, success, response_data, error_msg, response_time_ms
    )


def log_workorder_list_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                             success: bool, response_data: Optional[Dict], 
                             error_msg: Optional[str], payload: Dict,
                             response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录工单列表请求日志（便捷函数）"""
    return RequestLogService.log_workorder_list_request(
        session, platform_endpoint, success, response_data, error_msg, payload, response_time_ms
    )


def log_workorder_detail_request(session: AuthSession, platform_endpoint: PlatformEndpoint, 
                                success: bool, response_data: Optional[Dict], 
                                error_msg: Optional[str], payload: Dict,
                                response_time_ms: int = 0) -> Optional[RequestLog]:
    """记录工单详情请求日志（便捷函数）"""
    return RequestLogService.log_workorder_detail_request(
        session, platform_endpoint, success, response_data, error_msg, payload, response_time_ms
    )
