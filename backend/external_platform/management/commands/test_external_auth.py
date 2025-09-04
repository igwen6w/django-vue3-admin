# -*- coding: utf-8 -*-

"""
测试外部平台认证系统的管理命令
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from external_platform.models import Platform
from external_platform.services.auth_service import AuthService
from external_platform.services.captcha_service import get_captcha_service
from external_platform.utils import get_platform_config


class Command(BaseCommand):
    help = '测试外部平台认证系统'

    def add_arguments(self, parser):
        parser.add_argument(
            '--platform',
            type=str,
            default='city_center_workorder',
            help='平台标识'
        )
        parser.add_argument(
            '--account',
            type=str,
            required=True,
            help='测试账户'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='测试密码'
        )
        parser.add_argument(
            '--create-platform',
            action='store_true',
            help='创建测试平台'
        )

    def handle(self, *args, **options):
        platform_sign = options['platform']
        account = options['account']
        password = options['password']
        create_platform = options['create_platform']

        self.stdout.write(f"开始测试外部平台认证系统")
        self.stdout.write(f"平台: {platform_sign}")
        self.stdout.write(f"账户: {account}")

        try:
            # 1. 创建或获取平台
            if create_platform:
                self._create_test_platform(platform_sign)

            # 2. 测试验证码服务
            self._test_captcha_service()

            # 3. 测试认证服务
            self._test_auth_service(platform_sign, account)

            # 4. 触发登录任务
            self._test_login_task(platform_sign, account, password)

            self.stdout.write(
                self.style.SUCCESS('外部平台认证系统测试完成')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'测试失败: {str(e)}')
            )

    def _create_test_platform(self, platform_sign):
        """创建测试平台"""
        self.stdout.write("创建测试平台...")
        
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            # 如果数据库中没有配置，创建默认配置
            self.stdout.write("数据库中未找到平台配置，创建默认配置...")
            
            with transaction.atomic():
                platform, created = Platform.objects.get_or_create(
                    sign=platform_sign,
                    defaults={
                        'name': '测试平台',
                        'base_url': 'https://example.com',
                        'captcha_type': 1004,
                        'session_timeout_hours': 24,
                        'retry_limit': 3,
                        'is_active': True,
                        'description': '测试用平台'
                    }
                )
                
                if created:
                    self.stdout.write(f"平台创建成功: {platform.name}")
                    self.stdout.write("请在Django Admin中完善平台配置")
                else:
                    self.stdout.write(f"平台已存在: {platform.name}")
        else:
            self.stdout.write(f"找到平台配置: {platform_config['name']}")

    def _test_captcha_service(self):
        """测试验证码服务"""
        self.stdout.write("测试验证码服务...")
        
        captcha_service = get_captcha_service()
        if captcha_service:
            # 测试查询余额
            balance_result = captcha_service.get_balance()
            if balance_result.get('err_no') == 0:
                self.stdout.write(f"验证码服务可用，余额: {balance_result.get('tifen', 0)}")
            else:
                self.stdout.write(f"验证码服务配置有误: {balance_result.get('err_str')}")
        else:
            self.stdout.write("验证码服务不可用，请检查配置")

    def _test_auth_service(self, platform_sign, account):
        """测试认证服务"""
        self.stdout.write("测试认证服务...")
        
        # 查询现有会话
        session = AuthService.get_valid_session(platform_sign, account)
        if session:
            session_info = AuthService.get_session_info(session)
            self.stdout.write(f"找到有效会话: {session_info}")
        else:
            self.stdout.write("未找到有效会话")

        # 查询即将过期的会话
        near_expiry_sessions = AuthService.get_sessions_near_expiry()
        self.stdout.write(f"即将过期的会话数量: {len(near_expiry_sessions)}")

        # 查询已过期的会话
        expired_sessions = AuthService.get_expired_sessions()
        self.stdout.write(f"已过期的会话数量: {len(expired_sessions)}")

    def _test_login_task(self, platform_sign, account, password):
        """测试登录任务"""
        self.stdout.write("触发登录任务...")
        
        task_id = AuthService.trigger_login_task(platform_sign, account, password)
        if task_id:
            self.stdout.write(f"登录任务已触发，任务ID: {task_id}")
            self.stdout.write("请通过以下命令查看任务状态:")
            self.stdout.write(f"celery -A your_project inspect active")
        else:
            self.stdout.write("登录任务触发失败")