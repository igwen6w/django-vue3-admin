# 平台网关SDK配置说明

## 概述

平台网关SDK提供了与外部平台的集成能力，支持自动登录、会话管理、验证码处理、API封装等功能。

## 配置要求

### 1. Django Settings配置

在 `backend/settings.py` 中已经添加了以下配置：

```python
# 在INSTALLED_APPS中添加
INSTALLED_APPS = [
    # ... 其他应用
    "gateway",  # 平台网关SDK
]

# 平台网关SDK配置
GATEWAY_SETTINGS = {
    'username': os.getenv('GATEWAY_USERNAME', ''),
    'password': os.getenv('GATEWAY_PASSWORD', ''),
    'base_url': os.getenv('GATEWAY_BASE_URL', ''),
    'captcha_base_url': os.getenv('GATEWAY_CAPTCHA_BASE_URL', ''),
    # ... 其他配置
}

# Celery任务调度配置已自动包含网关相关任务
```

### 2. 环境变量配置

根据不同环境，在对应的 `.env` 文件中配置：

#### 必需配置项：
```bash
# 基础认证配置
GATEWAY_USERNAME='your_platform_username'
GATEWAY_PASSWORD='your_platform_password'
GATEWAY_BASE_URL='https://platform.example.com'
GATEWAY_CAPTCHA_BASE_URL='https://platform.example.com/captcha'
```

#### 可选配置项：
```bash
# 请求配置
GATEWAY_REQUEST_TIMEOUT=30
GATEWAY_SESSION_TIMEOUT=3600
GATEWAY_MAX_RETRIES=3
GATEWAY_REDIS_KEY_PREFIX='gateway:'

# 验证码配置
GATEWAY_CAPTCHA_TYPE=1004
GATEWAY_CAPTCHA_MAX_RETRIES=3

# Celery任务调度配置（秒）
GATEWAY_KEEPALIVE_INTERVAL=300           # 保活任务间隔
GATEWAY_HEALTH_CHECK_INTERVAL=600        # 健康检查间隔
GATEWAY_CLEANUP_INTERVAL=3600            # 清理任务间隔
GATEWAY_CONNECTIVITY_TEST_INTERVAL=1800  # 连通性测试间隔

# 任务开关
GATEWAY_ENABLE_KEEPALIVE_TASK=True
GATEWAY_ENABLE_HEALTH_CHECK_TASK=True
GATEWAY_ENABLE_CLEANUP_TASK=True
GATEWAY_ENABLE_CONNECTIVITY_TEST_TASK=True
```

### 3. 超级鹰验证码服务配置

```bash
CHAOJIYING_USERNAME='your_username'
CHAOJIYING_PASSWORD='your_password'
CHAOJIYING_SOFTWARE_ID='your_software_id'
```

## 不同环境的配置差异

### 开发环境 (.env.dev)
- 保活间隔较长（5分钟）
- 启用所有调试功能
- 连接开发平台URL

### 生产环境 (.env.prod)
- 保活间隔较短（3分钟）
- 优化性能配置
- 连接生产平台URL

### 示例环境 (.env.example)
- 提供完整的配置模板
- 包含所有可配置项的说明

## 配置验证

### 运行验证脚本
```bash
cd backend
python validate_gateway_config.py
```

### 使用管理命令验证
```bash
python manage.py gateway_manage config validate
```

## 使用示例

### 基础使用
```python
from gateway import get_user_info, submit_order, keepalive

# 获取用户信息
user_info = get_user_info()

# 提交订单
order_result = submit_order({'type': 'purchase', 'amount': 100})

# 手动保活
keepalive_result = keepalive()
```

### 高级使用
```python
from gateway import get_api_instance, execute_keepalive_now

# 获取API实例
api = get_api_instance()

# 健康检查
health_status = api.health_check()

# 手动触发保活任务
task_id = execute_keepalive_now(force_refresh=True)
```

## 故障排查

### 1. 配置验证失败
- 检查环境变量是否正确设置
- 确认Django settings是否包含GATEWAY_SETTINGS
- 验证必需字段是否都已配置

### 2. 验证码服务不可用
- 检查CHAOJIYING_CONFIG配置
- 确认超级鹰服务可访问性
- 验证账户余额和权限

### 3. Celery任务不执行
- 确认Celery Worker正在运行
- 检查Celery Beat调度器状态
- 验证Redis连接可用性

### 4. 会话管理问题
- 检查Redis连接配置
- 确认会话存储键前缀设置
- 验证平台登录凭据

## 监控和维护

### 管理命令
```bash
# 手动保活
python manage.py gateway_manage keepalive --force-refresh

# 健康检查
python manage.py gateway_manage health --detailed

# 会话管理
python manage.py gateway_manage session info
python manage.py gateway_manage session cleanup

# 任务状态
python manage.py gateway_manage task status
```

### 日志监控
- 查看Django日志中的gateway相关信息
- 监控Celery任务执行日志
- 关注Redis连接状态

## 更新说明

本次配置更新包含：

1. **Django Settings集成**: 将gateway应用添加到INSTALLED_APPS
2. **环境变量统一**: 所有环境文件包含完整的网关配置
3. **Celery任务调度**: 自动配置网关相关的定时任务
4. **配置验证工具**: 提供验证脚本和管理命令
5. **文档完善**: 详细的配置说明和使用指南

确保在部署前运行配置验证，并根据实际环境调整相关参数。