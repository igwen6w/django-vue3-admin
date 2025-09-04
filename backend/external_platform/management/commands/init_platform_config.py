# -*- coding: utf-8 -*-

"""
初始化外部平台配置数据的管理命令
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from external_platform.models import Platform, PlatformEndpoint, PlatformConfig


class Command(BaseCommand):
    help = '初始化外部平台配置数据'

    def handle(self, *args, **options):
        self.stdout.write("开始初始化外部平台配置数据...")

        try:
            with transaction.atomic():
                self._create_city_center_workorder_platform()
            
            self.stdout.write(
                self.style.SUCCESS('外部平台配置数据初始化完成')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'初始化失败: {str(e)}')
            )

    def _create_city_center_workorder_platform(self):
        """创建市中心工单系统平台配置"""
        self.stdout.write("创建市中心工单系统平台配置...")
        
        # 创建平台
        platform, created = Platform.objects.get_or_create(
            sign='city_center_workorder',
            defaults={
                'name': '市中心工单系统',
                'base_url': 'https://workorder.citycenter.gov.cn',
                'captcha_type': 1004,
                'session_timeout_hours': 24,
                'retry_limit': 3,
                'is_active': True,
                'description': '市中心工单管理系统'
            }
        )
        
        if created:
            self.stdout.write(f"✓ 平台创建成功: {platform.name}")
        else:
            self.stdout.write(f"✓ 平台已存在: {platform.name}")
        
        # 创建端点配置
        endpoints = [
            ('captcha', '/captcha', 'GET'),
            ('login', '/login', 'POST'),
            ('check_status', '/user/info', 'GET'),
            ('workorder_list', '/api/workorder/list', 'GET'),
        ]
        
        for endpoint_type, path, method in endpoints:
            endpoint, created = PlatformEndpoint.objects.get_or_create(
                platform=platform,
                endpoint_type=endpoint_type,
                defaults={
                    'path': path,
                    'http_method': method,
                    'description': f'{platform.name} {endpoint_type} 端点'
                }
            )
            
            if created:
                self.stdout.write(f"  ✓ 端点创建成功: {endpoint_type}")
            else:
                self.stdout.write(f"  ✓ 端点已存在: {endpoint_type}")
        
        # 创建额外配置
        extra_configs = [
            ('login_data_extra', {'remember': '1'}, '登录时的额外参数'),
        ]
        
        for config_key, config_value, description in extra_configs:
            config, created = PlatformConfig.objects.get_or_create(
                platform=platform,
                config_key=config_key,
                defaults={
                    'config_value': config_value,
                    'description': description
                }
            )
            
            if created:
                self.stdout.write(f"  ✓ 配置创建成功: {config_key}")
            else:
                self.stdout.write(f"  ✓ 配置已存在: {config_key}")