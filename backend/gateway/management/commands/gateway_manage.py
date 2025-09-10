# -*- coding: utf-8 -*-

"""
平台网关SDK管理命令
提供手动执行保活任务、健康检查、会话管理等功能
"""

import json
import time
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from gateway.tasks import (
    execute_keepalive_now, execute_health_check_now, execute_cleanup_now,
    keepalive_task, session_health_check_task, session_cleanup_task, test_connectivity_task
)
from gateway.api_wrappers import get_api_instance, reset_api_instance
from gateway.celery_config import validate_celery_config, get_task_status_summary


class Command(BaseCommand):
    """网关管理命令"""
    
    help = '平台网关SDK管理命令 - 执行保活任务、健康检查、会话管理等操作'
    
    def add_arguments(self, parser):
        """添加命令参数"""
        subparsers = parser.add_subparsers(dest='action', help='可用操作')
        
        # 保活相关命令
        keepalive_parser = subparsers.add_parser('keepalive', help='保活相关操作')
        keepalive_parser.add_argument(
            '--force-refresh', 
            action='store_true',
            help='强制刷新会话'
        )
        keepalive_parser.add_argument(
            '--async', 
            action='store_true',
            help='异步执行（使用Celery）'
        )
        
        # 健康检查命令
        health_parser = subparsers.add_parser('health', help='健康检查')
        health_parser.add_argument(
            '--async', 
            action='store_true',
            help='异步执行（使用Celery）'
        )
        health_parser.add_argument(
            '--detailed',
            action='store_true', 
            help='显示详细信息'
        )
        
        # 会话管理命令
        session_parser = subparsers.add_parser('session', help='会话管理')
        session_subparsers = session_parser.add_subparsers(dest='session_action', help='会话操作')
        
        # 会话信息
        session_subparsers.add_parser('info', help='显示会话信息')
        
        # 会话刷新
        session_subparsers.add_parser('refresh', help='刷新会话')
        
        # 会话清理
        cleanup_parser = session_subparsers.add_parser('cleanup', help='清理过期会话')
        cleanup_parser.add_argument(
            '--max-age-hours',
            type=int,
            default=24,
            help='最大保留时长（小时），默认24小时'
        )
        cleanup_parser.add_argument(
            '--async',
            action='store_true',
            help='异步执行（使用Celery）'
        )
        
        # 会话重置
        session_subparsers.add_parser('reset', help='重置API实例')
        
        # 任务管理命令
        task_parser = subparsers.add_parser('task', help='任务管理')
        task_subparsers = task_parser.add_subparsers(dest='task_action', help='任务操作')
        
        # 任务状态
        task_subparsers.add_parser('status', help='显示任务状态')
        
        # 任务配置验证
        task_subparsers.add_parser('validate', help='验证任务配置')
        
        # 连通性测试
        connectivity_parser = subparsers.add_parser('connectivity', help='连通性测试')
        connectivity_parser.add_argument(
            '--async',
            action='store_true',
            help='异步执行（使用Celery）'
        )
        
        # 配置管理
        config_parser = subparsers.add_parser('config', help='配置管理')
        config_subparsers = config_parser.add_subparsers(dest='config_action', help='配置操作')
        config_subparsers.add_parser('show', help='显示当前配置')
        config_subparsers.add_parser('validate', help='验证配置')
    
    def handle(self, *args, **options):
        """处理命令"""
        action = options.get('action')
        
        if not action:
            self.print_help('manage.py', 'gateway_manage')
            return
        
        try:
            if action == 'keepalive':
                self._handle_keepalive(options)
            elif action == 'health':
                self._handle_health(options)
            elif action == 'session':
                self._handle_session(options)
            elif action == 'task':
                self._handle_task(options)
            elif action == 'connectivity':
                self._handle_connectivity(options)
            elif action == 'config':
                self._handle_config(options)
            else:
                raise CommandError(f'未知操作: {action}')
                
        except Exception as e:
            raise CommandError(f'命令执行失败: {e}')
    
    def _handle_keepalive(self, options):
        """处理保活命令"""
        force_refresh = options.get('force_refresh', False)
        async_exec = options.get('async', False)
        
        self.stdout.write(f'执行保活任务 - force_refresh: {force_refresh}, async: {async_exec}')
        
        if async_exec:
            # 异步执行
            task_id = execute_keepalive_now(force_refresh=force_refresh)
            self.stdout.write(
                self.style.SUCCESS(f'保活任务已提交 - task_id: {task_id}')
            )
        else:
            # 同步执行
            start_time = time.time()
            result = keepalive_task(force_refresh=force_refresh)
            duration = time.time() - start_time
            
            if result.get('success'):
                self.stdout.write(
                    self.style.SUCCESS(f'保活任务执行成功 - 耗时: {duration:.2f}s')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'保活任务执行失败: {result.get("error")}')
                )
            
            self._print_json_result(result)
    
    def _handle_health(self, options):
        """处理健康检查命令"""
        async_exec = options.get('async', False)
        detailed = options.get('detailed', False)
        
        self.stdout.write(f'执行健康检查 - async: {async_exec}, detailed: {detailed}')
        
        if async_exec:
            # 异步执行
            task_id = execute_health_check_now()
            self.stdout.write(
                self.style.SUCCESS(f'健康检查任务已提交 - task_id: {task_id}')
            )
        else:
            # 同步执行
            start_time = time.time()
            result = session_health_check_task()
            duration = time.time() - start_time
            
            if result.get('success'):
                overall_health = result.get('overall_health', 'unknown')
                health_score = result.get('health_score', '0/0')
                warnings = result.get('warnings', [])
                
                self.stdout.write(
                    self.style.SUCCESS(f'健康检查完成 - 状态: {overall_health}, 评分: {health_score}')
                )
                
                if warnings:
                    self.stdout.write(
                        self.style.WARNING(f'发现问题: {", ".join(warnings)}')
                    )
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'健康检查失败: {result.get("error")}')
                )
            
            if detailed:
                self._print_json_result(result)
    
    def _handle_session(self, options):
        """处理会话管理命令"""
        session_action = options.get('session_action')
        
        if not session_action:
            self.stdout.write(self.style.ERROR('请指定会话操作'))
            return
        
        if session_action == 'info':
            self._show_session_info()
        elif session_action == 'refresh':
            self._refresh_session()
        elif session_action == 'cleanup':
            self._cleanup_session(options)
        elif session_action == 'reset':
            self._reset_session()
        else:
            self.stdout.write(self.style.ERROR(f'未知会话操作: {session_action}'))
    
    def _show_session_info(self):
        """显示会话信息"""
        try:
            api = get_api_instance()
            session_info = api.get_session_info()
            
            self.stdout.write(self.style.SUCCESS('会话信息:'))
            self._print_json_result(session_info)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'获取会话信息失败: {e}'))
    
    def _refresh_session(self):
        """刷新会话"""
        try:
            self.stdout.write('开始刷新会话...')
            
            api = get_api_instance()
            start_time = time.time()
            success = api.refresh_session()
            duration = time.time() - start_time
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'会话刷新成功 - 耗时: {duration:.2f}s')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('会话刷新失败')
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'会话刷新异常: {e}'))
    
    def _cleanup_session(self, options):
        """清理会话"""
        max_age_hours = options.get('max_age_hours', 24)
        async_exec = options.get('async', False)
        
        self.stdout.write(f'执行会话清理 - max_age: {max_age_hours}h, async: {async_exec}')
        
        if async_exec:
            # 异步执行
            task_id = execute_cleanup_now(max_age_hours=max_age_hours)
            self.stdout.write(
                self.style.SUCCESS(f'清理任务已提交 - task_id: {task_id}')
            )
        else:
            # 同步执行
            start_time = time.time()
            result = session_cleanup_task(max_age_hours=max_age_hours)
            duration = time.time() - start_time
            
            if result.get('success'):
                cleaned_count = result.get('cleaned_count', 0)
                total_checked = result.get('total_keys_checked', 0)
                
                self.stdout.write(
                    self.style.SUCCESS(f'会话清理完成 - 清理: {cleaned_count}, 检查: {total_checked}, 耗时: {duration:.2f}s')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'会话清理失败: {result.get("error")}')
                )
            
            self._print_json_result(result)
    
    def _reset_session(self):
        """重置会话"""
        try:
            self.stdout.write('重置API实例...')
            
            reset_api_instance()
            
            self.stdout.write(self.style.SUCCESS('API实例重置完成'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'API实例重置失败: {e}'))
    
    def _handle_task(self, options):
        """处理任务管理命令"""
        task_action = options.get('task_action')
        
        if not task_action:
            self.stdout.write(self.style.ERROR('请指定任务操作'))
            return
        
        if task_action == 'status':
            self._show_task_status()
        elif task_action == 'validate':
            self._validate_task_config()
        else:
            self.stdout.write(self.style.ERROR(f'未知任务操作: {task_action}'))
    
    def _show_task_status(self):
        """显示任务状态"""
        try:
            status_summary = get_task_status_summary()
            
            self.stdout.write(self.style.SUCCESS('任务状态汇总:'))
            self._print_json_result(status_summary)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'获取任务状态失败: {e}'))
    
    def _validate_task_config(self):
        """验证任务配置"""
        try:
            validation_result = validate_celery_config()
            
            if validation_result['valid']:
                self.stdout.write(self.style.SUCCESS('任务配置验证通过'))
            else:
                self.stdout.write(self.style.ERROR('任务配置验证失败'))
            
            # 显示详细验证结果
            self._print_json_result(validation_result)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'配置验证异常: {e}'))
    
    def _handle_connectivity(self, options):
        """处理连通性测试命令"""
        async_exec = options.get('async', False)
        
        self.stdout.write(f'执行连通性测试 - async: {async_exec}')
        
        if async_exec:
            # 异步执行
            result = test_connectivity_task.delay()
            self.stdout.write(
                self.style.SUCCESS(f'连通性测试任务已提交 - task_id: {result.id}')
            )
        else:
            # 同步执行
            start_time = time.time()
            result = test_connectivity_task()
            duration = time.time() - start_time
            
            if result.get('success'):
                response_time = result.get('response_time', 0)
                status_code = result.get('status_code', 0)
                
                self.stdout.write(
                    self.style.SUCCESS(f'连通性测试成功 - HTTP {status_code}, 响应时间: {response_time:.3f}s')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'连通性测试失败: {result.get("error")}')
                )
            
            self._print_json_result(result)
    
    def _handle_config(self, options):
        """处理配置管理命令"""
        config_action = options.get('config_action')
        
        if not config_action:
            self.stdout.write(self.style.ERROR('请指定配置操作'))
            return
        
        if config_action == 'show':
            self._show_config()
        elif config_action == 'validate':
            self._validate_config()
        else:
            self.stdout.write(self.style.ERROR(f'未知配置操作: {config_action}'))
    
    def _show_config(self):
        """显示当前配置"""
        try:
            from gateway.config import get_gateway_config
            
            config = get_gateway_config()
            config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
            
            # 隐藏敏感信息
            safe_config = {}
            for key, value in config_dict.items():
                if 'password' in key.lower() or 'secret' in key.lower() or 'key' in key.lower():
                    safe_config[key] = '***'
                else:
                    safe_config[key] = value
            
            self.stdout.write(self.style.SUCCESS('当前配置:'))
            self._print_json_result(safe_config)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'获取配置失败: {e}'))
    
    def _validate_config(self):
        """验证配置"""
        try:
            from gateway.config import get_gateway_config
            
            config = get_gateway_config()
            
            # 检查必需字段
            required_fields = ['username', 'password', 'base_url', 'captcha_base_url']
            missing_fields = []
            
            for field in required_fields:
                if not config.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                self.stdout.write(
                    self.style.ERROR(f'配置验证失败 - 缺少必需字段: {missing_fields}')
                )
            else:
                self.stdout.write(self.style.SUCCESS('配置验证通过'))
            
            # 验证Celery配置
            celery_validation = validate_celery_config()
            if celery_validation['valid']:
                self.stdout.write(self.style.SUCCESS('Celery配置验证通过'))
            else:
                self.stdout.write(
                    self.style.ERROR(f'Celery配置验证失败: {celery_validation["errors"]}')
                )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'配置验证异常: {e}'))
    
    def _print_json_result(self, data):
        """格式化打印JSON结果"""
        try:
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False, default=str)
            self.stdout.write(formatted_json)
        except Exception as e:
            self.stdout.write(f'数据格式化失败: {e}')
            self.stdout.write(str(data))