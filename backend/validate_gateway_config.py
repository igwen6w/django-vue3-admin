#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网关配置验证脚本
用于验证Django settings中的网关配置是否正确
"""

import os
import sys
import django
from pathlib import Path

# 设置Django环境
sys.path.append('/Users/19v/workspace/python/django-vue3-admin/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def validate_gateway_config():
    """验证网关配置"""
    print("开始验证网关配置...")
    
    try:
        from gateway.config import get_gateway_config, is_chaojiying_available
        from gateway.celery_config import validate_celery_config
        
        # 验证基础配置
        print("\n1. 验证基础配置...")
        config = get_gateway_config()
        
        required_fields = ['username', 'password', 'base_url', 'captcha_base_url']
        for field in required_fields:
            value = config.get(field)
            if value:
                print(f"   ✓ {field}: {'*' * 8 if 'password' in field else value}")
            else:
                print(f"   ✗ {field}: 未配置")
        
        # 验证超级鹰配置
        print("\n2. 验证超级鹰配置...")
        if is_chaojiying_available():
            chaojiying_config = config.get_chaojiying_config()
            print(f"   ✓ username: {chaojiying_config.get('username', '未配置')}")
            print(f"   ✓ password: {'*' * 8 if chaojiying_config.get('password') else '未配置'}")
            print(f"   ✓ software_id: {chaojiying_config.get('software_id', '未配置')}")
        else:
            print("   ✗ 超级鹰配置不可用")
        
        # 验证Celery配置
        print("\n3. 验证Celery配置...")
        celery_validation = validate_celery_config()
        
        if celery_validation['valid']:
            print("   ✓ Celery配置验证通过")
            
            config_summary = celery_validation.get('config_summary', {})
            for key, value in config_summary.items():
                print(f"   - {key}: {value}秒")
        else:
            print("   ✗ Celery配置验证失败")
            for error in celery_validation.get('errors', []):
                print(f"     - {error}")
        
        # 显示警告
        for warning in celery_validation.get('warnings', []):
            print(f"   ⚠ {warning}")
        
        # 验证任务开关
        print("\n4. 验证任务开关...")
        task_switches = [
            'enable_keepalive_task',
            'enable_health_check_task', 
            'enable_cleanup_task',
            'enable_connectivity_test_task'
        ]
        
        for switch in task_switches:
            value = config.get(switch, False)
            status = "启用" if value else "禁用"
            print(f"   - {switch}: {status}")
        
        print("\n✓ 配置验证完成")
        
    except Exception as e:
        print(f"\n✗ 配置验证失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    validate_gateway_config()