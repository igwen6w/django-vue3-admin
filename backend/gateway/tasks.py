# -*- coding: utf-8 -*-

"""
平台网关SDK Celery保活任务
实现自动保活机制，维持会话活跃状态，防止会话过期
"""

import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from celery import shared_task
from django.utils import timezone

from .api_wrappers import get_api_instance, reset_api_instance
from .exceptions import (
    GatewayError, AuthenticationError, SessionExpiredError,
    PlatformUnavailableError, ConfigurationError
)
from .config import get_gateway_config
from .utils import format_duration, safe_get_config

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def keepalive_task(self, force_refresh: bool = False) -> Dict[str, Any]:
    """Celery保活任务
    
    定期执行以维持会话活跃状态，防止会话过期。
    支持自动重试和错误恢复机制。
    
    Args:
        force_refresh: 是否强制刷新会话
        
    Returns:
        任务执行结果
    """
    task_start_time = time.time()
    task_id = self.request.id
    retry_count = self.request.retries
    
    logger.info(f"开始执行保活任务 - task_id: {task_id}, retry: {retry_count}, force_refresh: {force_refresh}")
    
    try:
        # 获取配置
        config = get_gateway_config()
        
        # 获取API实例
        api = get_api_instance()
        
        # 检查会话状态
        session_info = api.get_session_info()
        session_valid = session_info.get('session', {}).get('is_valid', False)
        
        logger.info(f"当前会话状态 - valid: {session_valid}, task_id: {task_id}")
        
        result = {
            'task_id': task_id,
            'start_time': task_start_time,
            'retry_count': retry_count,
            'force_refresh': force_refresh,
            'initial_session_valid': session_valid
        }
        
        # 如果强制刷新或会话无效，执行刷新
        if force_refresh or not session_valid:
            logger.info(f"执行会话刷新 - task_id: {task_id}")
            
            refresh_start = time.time()
            refresh_success = api.refresh_session()
            refresh_duration = time.time() - refresh_start
            
            result.update({
                'refresh_executed': True,
                'refresh_success': refresh_success,
                'refresh_duration': refresh_duration
            })
            
            if not refresh_success:
                error_msg = f"会话刷新失败 - task_id: {task_id}"
                logger.error(error_msg)
                
                # 重置API实例并重试
                reset_api_instance()
                
                raise SessionExpiredError(error_msg, details={
                    'task_id': task_id,
                    'retry_count': retry_count
                })
        
        # 执行保活请求
        keepalive_start = time.time()
        keepalive_result = api.keepalive()
        keepalive_duration = time.time() - keepalive_start
        
        keepalive_success = keepalive_result.get('success', False)
        
        result.update({
            'keepalive_executed': True,
            'keepalive_success': keepalive_success,
            'keepalive_duration': keepalive_duration,
            'keepalive_data': keepalive_result.get('data', {})
        })
        
        if not keepalive_success:
            error_msg = f"保活请求失败 - task_id: {task_id}"
            logger.warning(error_msg)
            
            # 如果是会话问题，尝试刷新会话
            if 'session' in str(keepalive_result.get('error', '')).lower():
                logger.info(f"检测到会话问题，尝试刷新 - task_id: {task_id}")
                
                refresh_success = api.refresh_session()
                if refresh_success:
                    # 重试保活请求
                    retry_keepalive_result = api.keepalive()
                    result.update({
                        'retry_keepalive_executed': True,
                        'retry_keepalive_success': retry_keepalive_result.get('success', False),
                        'retry_keepalive_data': retry_keepalive_result.get('data', {})
                    })
                    
                    if not retry_keepalive_result.get('success', False):
                        raise PlatformUnavailableError(f"重试保活请求仍然失败 - task_id: {task_id}")
                else:
                    raise AuthenticationError(f"会话刷新失败，无法执行保活 - task_id: {task_id}")
            else:
                raise PlatformUnavailableError(f"保活请求失败 - task_id: {task_id}")
        
        # 获取最终会话状态
        final_session_info = api.get_session_info()
        final_session_valid = final_session_info.get('session', {}).get('is_valid', False)
        
        # 记录任务统计
        task_duration = time.time() - task_start_time
        
        result.update({
            'final_session_valid': final_session_valid,
            'task_duration': task_duration,
            'task_duration_formatted': format_duration(task_duration),
            'success': True,
            'completed_at': timezone.now().isoformat(),
            'api_stats': final_session_info.get('api_stats', {})
        })
        
        logger.info(f"保活任务执行成功 - task_id: {task_id}, 耗时: {format_duration(task_duration)}")
        
        return result
        
    except (AuthenticationError, SessionExpiredError, PlatformUnavailableError) as e:
        # 这些异常需要重试
        logger.warning(f"保活任务遇到可重试错误 - task_id: {task_id}, retry: {retry_count}, error: {e}")
        
        if retry_count < self.max_retries:
            # 计算重试延迟（指数退避）
            retry_delay = min(60 * (2 ** retry_count), 300)  # 最大5分钟
            
            logger.info(f"保活任务将在{retry_delay}秒后重试 - task_id: {task_id}")
            
            raise self.retry(countdown=retry_delay, exc=e)
        else:
            # 重试次数用完，记录错误
            error_result = {
                'task_id': task_id,
                'start_time': task_start_time,
                'retry_count': retry_count,
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'task_duration': time.time() - task_start_time,
                'max_retries_exceeded': True
            }
            
            logger.error(f"保活任务重试次数用完，任务失败 - task_id: {task_id}, error: {e}")
            return error_result
            
    except Exception as e:
        # 其他异常，不重试
        error_result = {
            'task_id': task_id,
            'start_time': task_start_time,
            'retry_count': retry_count,
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'task_duration': time.time() - task_start_time,
            'non_retryable_error': True
        }
        
        logger.error(f"保活任务遇到不可重试错误 - task_id: {task_id}, error: {e}")
        return error_result


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def session_health_check_task(self) -> Dict[str, Any]:
    """会话健康检查任务
    
    定期检查会话健康状态，提前发现问题
    
    Returns:
        健康检查结果
    """
    task_start_time = time.time()
    task_id = self.request.id
    retry_count = self.request.retries
    
    logger.info(f"开始执行会话健康检查任务 - task_id: {task_id}, retry: {retry_count}")
    
    try:
        # 获取API实例
        api = get_api_instance()
        
        # 执行健康检查
        health_result = api.health_check()
        
        # 分析健康状态
        overall_health = health_result.get('overall_health', 'unknown')
        health_score = health_result.get('health_score', '0/0')
        
        # 检查是否需要预警
        warnings = []
        
        if health_result.get('session_manager') != 'healthy':
            warnings.append('SessionManager状态异常')
        
        if health_result.get('redis_connection') != 'healthy':
            warnings.append('Redis连接异常')
        
        if health_result.get('platform_connectivity') != 'healthy':
            warnings.append('平台连通性异常')
        
        # 检查会话过期时间
        session_info = health_result.get('session', {})
        expires_at_str = session_info.get('expires_at')
        if expires_at_str:
            try:
                expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                time_to_expire = (expires_at - timezone.now()).total_seconds()
                
                # 如果会话在30分钟内过期，发出预警
                if time_to_expire < 1800:
                    warnings.append(f'会话将在{format_duration(time_to_expire)}后过期')
            except (ValueError, TypeError):
                warnings.append('无法解析会话过期时间')
        
        task_duration = time.time() - task_start_time
        
        result = {
            'task_id': task_id,
            'task_duration': task_duration,
            'overall_health': overall_health,
            'health_score': health_score,
            'warnings': warnings,
            'health_details': health_result,
            'requires_attention': len(warnings) > 0,
            'completed_at': timezone.now().isoformat(),
            'success': True
        }
        
        if warnings:
            logger.warning(f"健康检查发现问题 - task_id: {task_id}, warnings: {warnings}")
        else:
            logger.info(f"健康检查通过 - task_id: {task_id}, health: {overall_health}")
        
        return result
        
    except Exception as e:
        logger.error(f"健康检查任务异常 - task_id: {task_id}, error: {e}")
        
        if retry_count < self.max_retries:
            retry_delay = 30 * (retry_count + 1)
            logger.info(f"健康检查任务将在{retry_delay}秒后重试 - task_id: {task_id}")
            raise self.retry(countdown=retry_delay, exc=e)
        else:
            return {
                'task_id': task_id,
                'task_duration': time.time() - task_start_time,
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'max_retries_exceeded': True
            }


@shared_task(bind=True, max_retries=1)
def session_cleanup_task(self, max_age_hours: int = 24) -> Dict[str, Any]:
    """会话清理任务
    
    清理过期的会话数据，释放Redis存储空间
    
    Args:
        max_age_hours: 最大保留时长（小时）
        
    Returns:
        清理结果
    """
    task_start_time = time.time()
    task_id = self.request.id
    
    logger.info(f"开始执行会话清理任务 - task_id: {task_id}, max_age: {max_age_hours}h")
    
    try:
        # 获取API实例
        api = get_api_instance()
        
        # 获取Redis客户端
        redis_client = api.session_manager.redis_client
        
        # 查找所有网关相关的键
        config = get_gateway_config()
        key_prefix = safe_get_config(config.to_dict() if hasattr(config, 'to_dict') else {}, 'redis_key_prefix', 'gateway:')
        
        pattern = f"{key_prefix}*"
        keys = redis_client.keys(pattern)
        
        cleaned_count = 0
        error_count = 0
        cutoff_time = timezone.now() - timedelta(hours=max_age_hours)
        
        for key in keys:
            try:
                # 检查键的TTL
                ttl = redis_client.ttl(key)
                
                if ttl == -1:  # 没有过期时间的键
                    # 检查数据内容判断是否过期
                    data_str = redis_client.get(key)
                    if data_str:
                        try:
                            import json
                            data = json.loads(data_str)
                            created_at_str = data.get('created_at')
                            
                            if created_at_str:
                                created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                                if created_at < cutoff_time:
                                    redis_client.delete(key)
                                    cleaned_count += 1
                                    logger.debug(f"清理过期会话数据: {key}")
                        except (json.JSONDecodeError, ValueError, TypeError):
                            # 无法解析的数据，如果超过保留期限则删除
                            redis_client.delete(key)
                            cleaned_count += 1
                            logger.debug(f"清理无效会话数据: {key}")
                
            except Exception as e:
                logger.warning(f"清理键时出错 - key: {key}, error: {e}")
                error_count += 1
        
        task_duration = time.time() - task_start_time
        
        result = {
            'task_id': task_id,
            'task_duration': task_duration,
            'total_keys_checked': len(keys),
            'cleaned_count': cleaned_count,
            'error_count': error_count,
            'max_age_hours': max_age_hours,
            'completed_at': timezone.now().isoformat(),
            'success': True
        }
        
        logger.info(f"会话清理任务完成 - task_id: {task_id}, 清理: {cleaned_count}, 检查: {len(keys)}")
        
        return result
        
    except Exception as e:
        logger.error(f"会话清理任务异常 - task_id: {task_id}, error: {e}")
        
        return {
            'task_id': task_id,
            'task_duration': time.time() - task_start_time,
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }


@shared_task
def test_connectivity_task() -> Dict[str, Any]:
    """连通性测试任务
    
    测试与平台的连通性，不涉及认证
    
    Returns:
        连通性测试结果
    """
    task_start_time = time.time()
    
    logger.info("开始执行连通性测试任务")
    
    try:
        import requests
        from .config import get_gateway_config
        
        config = get_gateway_config()
        base_url = config.get('base_url')
        
        if not base_url:
            raise ConfigurationError("BASE_URL配置未设置")
        
        # 执行简单的连通性测试
        test_url = f"{base_url.rstrip('/')}/ping"  # 假设有ping接口
        
        response = requests.get(test_url, timeout=10)
        
        result = {
            'success': True,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'platform_url': base_url,
            'test_url': test_url,
            'task_duration': time.time() - task_start_time,
            'completed_at': timezone.now().isoformat()
        }
        
        logger.info(f"连通性测试完成 - status: {response.status_code}, time: {response.elapsed.total_seconds():.3f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"连通性测试失败: {e}")
        
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'task_duration': time.time() - task_start_time,
            'completed_at': timezone.now().isoformat()
        }


# 任务调度配置辅助函数
def get_default_schedule_config() -> Dict[str, Any]:
    """获取默认的任务调度配置
    
    Returns:
        Celery Beat调度配置
    """
    config = get_gateway_config()
    
    # 从配置中获取调度间隔，默认值如下
    keepalive_interval = safe_get_config(
        config.to_dict() if hasattr(config, 'to_dict') else {}, 
        'keepalive_interval', 
        300  # 默认5分钟
    )
    
    health_check_interval = safe_get_config(
        config.to_dict() if hasattr(config, 'to_dict') else {},
        'health_check_interval',
        600  # 默认10分钟
    )
    
    cleanup_interval = safe_get_config(
        config.to_dict() if hasattr(config, 'to_dict') else {},
        'cleanup_interval',
        3600  # 默认1小时
    )
    
    connectivity_test_interval = safe_get_config(
        config.to_dict() if hasattr(config, 'to_dict') else {},
        'connectivity_test_interval',
        1800  # 默认30分钟
    )
    
    return {
        'gateway-keepalive': {
            'task': 'gateway.tasks.keepalive_task',
            'schedule': keepalive_interval,
            'options': {
                'queue': 'gateway',
                'routing_key': 'gateway.keepalive'
            }
        },
        'gateway-health-check': {
            'task': 'gateway.tasks.session_health_check_task',
            'schedule': health_check_interval,
            'options': {
                'queue': 'gateway',
                'routing_key': 'gateway.health'
            }
        },
        'gateway-session-cleanup': {
            'task': 'gateway.tasks.session_cleanup_task',
            'schedule': cleanup_interval,
            'options': {
                'queue': 'gateway',
                'routing_key': 'gateway.cleanup'
            }
        },
        'gateway-connectivity-test': {
            'task': 'gateway.tasks.test_connectivity_task',
            'schedule': connectivity_test_interval,
            'options': {
                'queue': 'gateway',
                'routing_key': 'gateway.connectivity'
            }
        }
    }


# 手动任务执行函数
def execute_keepalive_now(force_refresh: bool = False) -> str:
    """立即执行保活任务
    
    Args:
        force_refresh: 是否强制刷新会话
        
    Returns:
        任务ID
    """
    result = keepalive_task.delay(force_refresh=force_refresh)
    logger.info(f"手动触发保活任务 - task_id: {result.id}, force_refresh: {force_refresh}")
    return result.id


def execute_health_check_now() -> str:
    """立即执行健康检查任务
    
    Returns:
        任务ID
    """
    result = session_health_check_task.delay()
    logger.info(f"手动触发健康检查任务 - task_id: {result.id}")
    return result.id


def execute_cleanup_now(max_age_hours: int = 24) -> str:
    """立即执行清理任务
    
    Args:
        max_age_hours: 最大保留时长
        
    Returns:
        任务ID
    """
    result = session_cleanup_task.delay(max_age_hours=max_age_hours)
    logger.info(f"手动触发清理任务 - task_id: {result.id}, max_age: {max_age_hours}h")
    return result.id