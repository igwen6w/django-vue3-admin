# -*- coding: utf-8 -*-

"""
外部平台认证相关的Celery异步任务
"""

import logging
import time
from typing import Dict, Any, Optional
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from external_platform.models import Platform, AuthSession, RequestLog, ExternalAuthCaptchaLog, PlatformEndpoint
from external_platform.choices import PlatformAuthStatus, ApiMethod
from external_platform.services.captcha_service import get_captcha_service
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.services.auth_service import AuthService
from external_platform.utils import get_platform_config, get_task_config

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def login_task(self, platform_sign: str, account: str, password: str) -> Dict[str, Any]:
    """异步登录任务
    
    Args:
        platform_sign: 平台标识
        account: 账户名
        password: 密码
        
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    logger.info(f"开始执行登录任务 - 任务ID: {task_id}, 平台: {platform_sign}, 账户: {account}")
    
    start_time = time.time()
    platform = None
    client = None
    
    try:
        # 获取平台配置
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"未找到平台配置: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 获取平台对象
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 初始化客户端
        client = ExternalPlatformClient(platform_config['base_url'])
        
        # 执行登录流程
        result = _execute_login_flow(
            task_id, platform, account, password, 
            platform_config, client
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        if result['success']:
            logger.info(f"登录任务完成 - 任务ID: {task_id}, 平台: {platform_sign}, "
                       f"账户: {account}, 耗时: {execution_time}ms")
        else:
            logger.error(f"登录任务失败 - 任务ID: {task_id}, 平台: {platform_sign}, "
                        f"账户: {account}, 耗时: {execution_time}ms, 错误: {result['error']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"登录任务异常: {str(e)}"
        logger.error(f"登录任务异常 - 任务ID: {task_id}, 平台: {platform_sign}, "
                    f"账户: {account}, 耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        
        # 记录失败日志
        if platform:
            _log_request_failure(platform, account, 'login', error_msg, execution_time)
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('login_task').get('retry_delay', 60)
            logger.info(f"登录任务重试 - 任务ID: {task_id}, 重试次数: {self.request.retries + 1}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return {'success': False, 'error': error_msg}
    
    finally:
        if client:
            client.close()


def _execute_login_flow(task_id: str, platform: Platform, account: str, 
                       password: str, platform_config: Dict, 
                       client: ExternalPlatformClient) -> Dict[str, Any]:
    """执行完整的登录流程
    
    Args:
        task_id: 任务ID
        platform: 平台对象
        account: 账户名
        password: 密码
        platform_config: 平台配置
        client: 外部平台客户端
        
    Returns:
        登录结果
    """
    logger.info(f"开始登录流程 - 任务ID: {task_id}, 平台: {platform.sign}, 账户: {account}")
    
    # 步骤1: 获取验证码
    captcha_endpoint = platform_config['endpoints']['captcha']
    captcha_image, cookies = client.get_captcha(captcha_endpoint)
    
    if not captcha_image or not cookies:
        error_msg = "获取验证码失败"
        _log_request_failure(platform, account, captcha_endpoint, error_msg)
        return {'success': False, 'error': error_msg}
    
    logger.info(f"验证码获取成功 - 任务ID: {task_id}, 图片大小: {len(captcha_image)} bytes")
    
    # 步骤2: 识别验证码
    captcha_service = get_captcha_service()
    if not captcha_service:
        error_msg = "验证码服务不可用"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
    
    captcha_type = platform_config.get('captcha_type', 1004)
    captcha_result = captcha_service.recognize_captcha(captcha_image, captcha_type)
    
    # 记录验证码识别日志
    request_log = _log_captcha_request(platform, account, captcha_endpoint, captcha_result)
    
    if captcha_result.get('err_no') != 0:
        error_msg = f"验证码识别失败: {captcha_result.get('err_str', '未知错误')}"
        logger.error(f"验证码识别失败 - 任务ID: {task_id}, 错误: {error_msg}")
        return {'success': False, 'error': error_msg}
    
    captcha_text = captcha_result.get('pic_str', '')
    pic_id = captcha_result.get('pic_id', '')
    
    logger.info(f"验证码识别成功 - 任务ID: {task_id}, 识别结果: {captcha_text}, pic_id: {pic_id}")
    
    # 记录验证码识别结果
    if request_log:
        _log_captcha_recognition(request_log, captcha_result)
    
    # 步骤3: 执行登录
    login_endpoint = platform_config['endpoints']['login']
    additional_data = platform_config.get('login_data_extra', {})
    
    success, response_cookies, error_msg = client.login(
        login_endpoint, account, password, captcha_text, cookies, additional_data
    )
    
    # 记录登录请求日志
    _log_login_request(platform, account, login_endpoint, success, error_msg, response_cookies)
    
    if not success:
        # 如果是验证码错误，报告给超级鹰
        if pic_id and ('验证码' in error_msg or 'captcha' in error_msg.lower()):
            captcha_service.report_error(pic_id)
            logger.info(f"已报告验证码错误 - pic_id: {pic_id}")
        
        return {'success': False, 'error': error_msg}
    
    # 步骤4: 合并Cookie并保存会话
    all_cookies = {**cookies, **response_cookies} if response_cookies else cookies
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


@shared_task
def maintain_auth_status_task() -> Dict[str, Any]:
    """维护认证状态的定时任务"""
    logger.info("开始执行认证状态维护任务")
    
    start_time = time.time()
    result = {
        'checked_count': 0,
        'refreshed_count': 0,
        'expired_count': 0,
        'error_count': 0
    }
    
    try:
        # 清理已过期的会话
        expired_count = AuthService.cleanup_expired_sessions()
        result['expired_count'] = expired_count
        
        # 获取即将过期的会话
        config = get_task_config('maintain_auth_status')
        refresh_before_hours = config.get('refresh_before_hours', 2)
        near_expiry_sessions = AuthService.get_sessions_near_expiry(refresh_before_hours)
        
        result['checked_count'] = len(near_expiry_sessions)
        
        # 触发刷新任务
        for session in near_expiry_sessions:
            try:
                # 这里可以触发刷新任务或直接检查状态
                # 暂时只记录，实际项目中可以根据需要实现自动刷新
                logger.info(f"会话即将过期 - 会话ID: {session.id}, "
                           f"平台: {session.platform.sign}, 账户: {session.account}, "
                           f"过期时间: {session.expire_time}")
                result['refreshed_count'] += 1
                
            except Exception as e:
                logger.error(f"处理即将过期会话失败 - 会话ID: {session.id}, "
                            f"错误: {str(e)}", exc_info=True)
                result['error_count'] += 1
        
        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"认证状态维护任务完成 - 耗时: {execution_time}ms, "
                   f"检查: {result['checked_count']}, 刷新: {result['refreshed_count']}, "
                   f"过期: {result['expired_count']}, 错误: {result['error_count']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"认证状态维护任务异常: {str(e)}"
        logger.error(f"认证状态维护任务异常 - 耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        result['error_count'] += 1
        return result


def _log_request_failure(platform: Platform, account: str, endpoint_path: str, 
                        error_msg: str, response_time_ms: int = 0):
    """记录请求失败日志"""
    try:
        # 尝试获取对应的平台端点配置
        platform_endpoint = None
        try:
            # 根据endpoint_path推断端点类型
            endpoint_type = None
            if 'captcha' in endpoint_path.lower():
                endpoint_type = 'captcha'
            elif 'login' in endpoint_path.lower():
                endpoint_type = 'login'
            
            if endpoint_type:
                platform_endpoint = PlatformEndpoint.objects.get(
                    platform=platform, 
                    endpoint_type=endpoint_type
                )
        except PlatformEndpoint.DoesNotExist:
            pass
        
        RequestLog.objects.create(
            platform=platform,
            platform_endpoint=platform_endpoint,
            account=account,
            endpoint_path=endpoint_path,
            method=ApiMethod.GET,
            status_code=500,
            error_message=error_msg,
            response_time_ms=response_time_ms,
            tag={'type': 'request_failure'}
        )
    except Exception as e:
        logger.error(f"记录请求失败日志异常: {str(e)}", exc_info=True)


def _log_captcha_request(platform: Platform, account: str, endpoint_path: str, 
                        captcha_result: Dict) -> Optional[RequestLog]:
    """记录验证码请求日志"""
    try:
        # 尝试获取对应的平台端点配置
        platform_endpoint = None
        try:
            platform_endpoint = PlatformEndpoint.objects.get(
                platform=platform, 
                endpoint_type='captcha'
            )
        except PlatformEndpoint.DoesNotExist:
            pass
        
        request_log = RequestLog.objects.create(
            platform=platform,
            platform_endpoint=platform_endpoint,
            account=account,
            endpoint_path=endpoint_path,
            method=ApiMethod.GET,
            status_code=200 if captcha_result.get('err_no') == 0 else 400,
            response_time_ms=0,  # 验证码请求通常不记录响应时间
            response_body=captcha_result,
            tag={'type': 'captcha_request'}
        )
        return request_log
    except Exception as e:
        logger.error(f"记录验证码请求日志异常: {str(e)}", exc_info=True)
        return None


def _log_captcha_recognition(request_log: RequestLog, captcha_result: Dict):
    """记录验证码识别结果"""
    try:
        ExternalAuthCaptchaLog.objects.create(
            request_log=request_log,
            # 这里可以添加更多验证码识别相关的字段
        )
    except Exception as e:
        logger.error(f"记录验证码识别日志异常: {str(e)}", exc_info=True)


def _log_login_request(platform: Platform, account: str, endpoint_path: str, 
                      success: bool, error_msg: Optional[str], 
                      response_cookies: Optional[Dict]):
    """记录登录请求日志"""
    try:
        # 尝试获取登录端点配置
        platform_endpoint = None
        try:
            platform_endpoint = PlatformEndpoint.objects.get(
                platform=platform, 
                endpoint_type='login'
            )
        except PlatformEndpoint.DoesNotExist:
            pass
        
        RequestLog.objects.create(
            platform=platform,
            platform_endpoint=platform_endpoint,
            account=account,
            endpoint_path=endpoint_path,
            method=ApiMethod.POST,
            status_code=200 if success else 400,
            response_body={'cookies': response_cookies} if response_cookies else None,
            error_message=error_msg if not success else None,
            tag={'type': 'login_request', 'success': success}
        )
    except Exception as e:
        logger.error(f"记录登录请求日志异常: {str(e)}", exc_info=True)