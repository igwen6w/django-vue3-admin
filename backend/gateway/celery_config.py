# -*- coding: utf-8 -*-

"""
平台网关SDK Celery配置
提供Celery Beat调度配置和任务路由配置
"""

import logging
from datetime import timedelta
from django.conf import settings

from .config import get_gateway_config
from .utils import safe_get_config

logger = logging.getLogger(__name__)


def get_gateway_celery_config() -> dict:
    """获取网关SDK的Celery配置
    
    Returns:
        Celery配置字典
    """
    try:
        config = get_gateway_config()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # 获取调度间隔配置
        keepalive_interval = safe_get_config(config_dict, 'keepalive_interval', 300)  # 5分钟
        health_check_interval = safe_get_config(config_dict, 'health_check_interval', 600)  # 10分钟
        cleanup_interval = safe_get_config(config_dict, 'cleanup_interval', 3600)  # 1小时
        connectivity_test_interval = safe_get_config(config_dict, 'connectivity_test_interval', 1800)  # 30分钟
        
        # 是否启用各类任务
        enable_keepalive = safe_get_config(config_dict, 'enable_keepalive_task', True)
        enable_health_check = safe_get_config(config_dict, 'enable_health_check_task', True)
        enable_cleanup = safe_get_config(config_dict, 'enable_cleanup_task', True)
        enable_connectivity_test = safe_get_config(config_dict, 'enable_connectivity_test_task', True)
        
        # 构建调度配置
        beat_schedule = {}
        
        if enable_keepalive:
            beat_schedule['gateway-keepalive'] = {
                'task': 'gateway.tasks.keepalive_task',
                'schedule': timedelta(seconds=keepalive_interval),
                'options': {
                    'queue': 'gateway',
                    'routing_key': 'gateway.keepalive',
                    'priority': 8  # 高优先级
                }
            }
        
        if enable_health_check:
            beat_schedule['gateway-health-check'] = {
                'task': 'gateway.tasks.session_health_check_task',
                'schedule': timedelta(seconds=health_check_interval),
                'options': {
                    'queue': 'gateway',
                    'routing_key': 'gateway.health',
                    'priority': 6  # 中等优先级
                }
            }
        
        if enable_cleanup:
            beat_schedule['gateway-session-cleanup'] = {
                'task': 'gateway.tasks.session_cleanup_task',
                'schedule': timedelta(seconds=cleanup_interval),
                'options': {
                    'queue': 'gateway',
                    'routing_key': 'gateway.cleanup',
                    'priority': 3  # 低优先级
                }
            }
        
        if enable_connectivity_test:
            beat_schedule['gateway-connectivity-test'] = {
                'task': 'gateway.tasks.test_connectivity_task',
                'schedule': timedelta(seconds=connectivity_test_interval),
                'options': {
                    'queue': 'gateway',
                    'routing_key': 'gateway.connectivity',
                    'priority': 4  # 低优先级
                }
            }
        
        # 任务路由配置
        task_routes = {
            'gateway.tasks.keepalive_task': {
                'queue': 'gateway',
                'routing_key': 'gateway.keepalive'
            },
            'gateway.tasks.session_health_check_task': {
                'queue': 'gateway', 
                'routing_key': 'gateway.health'
            },
            'gateway.tasks.session_cleanup_task': {
                'queue': 'gateway',
                'routing_key': 'gateway.cleanup'
            },
            'gateway.tasks.test_connectivity_task': {
                'queue': 'gateway',
                'routing_key': 'gateway.connectivity'
            }
        }
        
        # 任务配置
        task_annotations = {
            'gateway.tasks.keepalive_task': {
                'rate_limit': '6/m',  # 每分钟最多6次，防止过于频繁
                'time_limit': 120,    # 2分钟超时
                'soft_time_limit': 90, # 90秒软超时
                'retry_backoff': True,
                'retry_backoff_max': 300,  # 最大重试间隔5分钟
                'retry_jitter': True
            },
            'gateway.tasks.session_health_check_task': {
                'rate_limit': '10/m',
                'time_limit': 60,
                'soft_time_limit': 45,
                'retry_backoff': True
            },
            'gateway.tasks.session_cleanup_task': {
                'rate_limit': '2/h',   # 每小时最多2次
                'time_limit': 300,     # 5分钟超时
                'soft_time_limit': 240
            },
            'gateway.tasks.test_connectivity_task': {
                'rate_limit': '4/m',
                'time_limit': 30,
                'soft_time_limit': 20
            }
        }
        
        celery_config = {
            'beat_schedule': beat_schedule,
            'task_routes': task_routes,
            'task_annotations': task_annotations,
            'timezone': getattr(settings, 'TIME_ZONE', 'UTC'),
            'enable_utc': True
        }
        
        logger.info(f"网关Celery配置加载完成 - 启用任务数: {len(beat_schedule)}")
        
        return celery_config
        
    except Exception as e:
        logger.error(f"加载网关Celery配置失败: {e}")
        return {}


def update_django_celery_config():
    """更新Django的Celery配置
    
    将网关SDK的配置合并到Django的Celery配置中
    """
    try:
        gateway_config = get_gateway_celery_config()
        
        if not gateway_config:
            logger.warning("网关Celery配置为空，跳过更新")
            return
        
        # 获取现有的Django Celery配置
        existing_beat_schedule = getattr(settings, 'CELERY_BEAT_SCHEDULE', {})
        existing_task_routes = getattr(settings, 'CELERY_TASK_ROUTES', {})
        existing_task_annotations = getattr(settings, 'CELERY_TASK_ANNOTATIONS', {})
        
        # 合并配置
        existing_beat_schedule.update(gateway_config.get('beat_schedule', {}))
        existing_task_routes.update(gateway_config.get('task_routes', {}))
        existing_task_annotations.update(gateway_config.get('task_annotations', {}))
        
        # 更新Django settings
        settings.CELERY_BEAT_SCHEDULE = existing_beat_schedule
        settings.CELERY_TASK_ROUTES = existing_task_routes
        settings.CELERY_TASK_ANNOTATIONS = existing_task_annotations
        
        # 设置时区配置
        if not hasattr(settings, 'CELERY_TIMEZONE'):
            settings.CELERY_TIMEZONE = gateway_config.get('timezone', 'UTC')
        
        if not hasattr(settings, 'CELERY_ENABLE_UTC'):
            settings.CELERY_ENABLE_UTC = gateway_config.get('enable_utc', True)
        
        logger.info("网关Celery配置已合并到Django配置中")
        
    except Exception as e:
        logger.error(f"更新Django Celery配置失败: {e}")


def get_task_status_summary() -> dict:
    """获取任务状态汇总
    
    Returns:
        任务状态汇总信息
    """
    try:
        from celery import current_app
        
        # 获取所有网关任务的状态
        gateway_tasks = [
            'gateway.tasks.keepalive_task',
            'gateway.tasks.session_health_check_task', 
            'gateway.tasks.session_cleanup_task',
            'gateway.tasks.test_connectivity_task'
        ]
        
        task_summary = {}
        
        for task_name in gateway_tasks:
            try:
                # 获取任务的活跃实例
                active_tasks = current_app.control.inspect().active()
                scheduled_tasks = current_app.control.inspect().scheduled()
                
                task_info = {
                    'task_name': task_name,
                    'active_count': 0,
                    'scheduled_count': 0,
                    'last_run': None
                }
                
                # 统计活跃任务
                if active_tasks:
                    for worker, tasks in active_tasks.items():
                        task_info['active_count'] += len([t for t in tasks if t['name'] == task_name])
                
                # 统计调度任务
                if scheduled_tasks:
                    for worker, tasks in scheduled_tasks.items():
                        task_info['scheduled_count'] += len([t for t in tasks if t['name'] == task_name])
                
                task_summary[task_name] = task_info
                
            except Exception as e:
                logger.warning(f"获取任务{task_name}状态失败: {e}")
                task_summary[task_name] = {
                    'task_name': task_name,
                    'error': str(e)
                }
        
        return {
            'summary': task_summary,
            'total_tasks': len(gateway_tasks),
            'timestamp': logger.log
        }
        
    except Exception as e:
        logger.error(f"获取任务状态汇总失败: {e}")
        return {'error': str(e)}


# Django应用启动时自动更新配置
def auto_configure_celery():
    """自动配置Celery（在Django启动时调用）"""
    try:
        # 检查是否启用了Celery
        if hasattr(settings, 'CELERY_BROKER_URL') and settings.CELERY_BROKER_URL:
            update_django_celery_config()
            logger.info("网关SDK Celery配置自动加载完成")
        else:
            logger.warning("Celery未配置，跳过网关任务调度设置")
    except Exception as e:
        logger.error(f"自动配置Celery失败: {e}")


# 配置验证函数
def validate_celery_config() -> dict:
    """验证Celery配置
    
    Returns:
        验证结果
    """
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'config_summary': {}
    }
    
    try:
        # 检查Django Celery基础配置
        if not hasattr(settings, 'CELERY_BROKER_URL'):
            validation_result['errors'].append('CELERY_BROKER_URL未配置')
            validation_result['valid'] = False
        
        if not hasattr(settings, 'CELERY_RESULT_BACKEND'):
            validation_result['warnings'].append('CELERY_RESULT_BACKEND未配置，任务结果将不会保存')
        
        # 检查网关配置
        try:
            config = get_gateway_config()
            config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
            
            validation_result['config_summary'] = {
                'keepalive_interval': safe_get_config(config_dict, 'keepalive_interval', 300),
                'health_check_interval': safe_get_config(config_dict, 'health_check_interval', 600),
                'cleanup_interval': safe_get_config(config_dict, 'cleanup_interval', 3600),
                'connectivity_test_interval': safe_get_config(config_dict, 'connectivity_test_interval', 1800)
            }
            
        except Exception as e:
            validation_result['errors'].append(f'网关配置加载失败: {e}')
            validation_result['valid'] = False
        
        # 检查Celery应用是否可用
        try:
            from celery import current_app
            current_app.control.inspect().ping()
        except Exception as e:
            validation_result['warnings'].append(f'Celery应用连接测试失败: {e}')
        
    except Exception as e:
        validation_result['errors'].append(f'配置验证异常: {e}')
        validation_result['valid'] = False
    
    return validation_result