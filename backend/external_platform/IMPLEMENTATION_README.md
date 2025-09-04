# 外部平台认证系统实现说明

## 系统概述

本系统实现了基于Celery异步任务的外部平台认证管理，主要用于市中心工单系统的自动登录和会话维护。

## 核心功能

1. **自动登录流程** - 获取验证码 → 超级鹰识别 → 提交登录 → 保存会话
2. **会话管理** - 检查会话有效性、自动过期处理、状态维护
3. **异步任务** - 登录任务、状态维护任务
4. **完整日志** - 请求日志、验证码识别日志、错误日志

## 配置要求

### 1. Django设置

所有配置已集中在`backend/settings.py`中：

```python
# 超级鹰验证码配置
CHAOJIYING_CONFIG = {
    'username': os.getenv('CHAOJIYING_USERNAME', ''),
    'password': os.getenv('CHAOJIYING_PASSWORD', ''),
    'software_id': os.getenv('CHAOJIYING_SOFTWARE_ID', ''),
    'timeout': 30
}

# 外部平台配置现在从数据库动态读取
# 使用 Platform, PlatformEndpoint, PlatformConfig 模型管理配置

# 外部平台任务配置
EXTERNAL_PLATFORM_TASK_CONFIG = {
    'login_task': {
        'max_retries': 3,
        'retry_delay': 60,
        'timeout': 300
    },
    'maintain_auth_status': {
        'check_interval_minutes': 10,
        'refresh_before_hours': 2,
        'batch_size': 50
    }
}



# Celery定时任务配置
CELERY_BEAT_SCHEDULE = {
    'maintain-auth-status': {
        'task': 'external_platform.tasks.maintain_auth_status_task',
        'schedule': 600,  # 每10分钟执行一次
    },
}
```

### 2. 数据库迁移

```bash
python manage.py makemigrations external_platform
python manage.py migrate
```

### 3. 初始化平台配置数据

```bash
# 运行初始化命令创建默认平台配置
python manage.py init_platform_config
```

或者手动创建：

```python
from external_platform.models import Platform, PlatformEndpoint, PlatformConfig

# 创建平台
platform = Platform.objects.create(
    name='市中心工单系统',
    sign='city_center_workorder',
    base_url='https://workorder.citycenter.gov.cn',
    captcha_type=1004,
    session_timeout_hours=24,
    retry_limit=3
)

# 创建端点配置
PlatformEndpoint.objects.create(
    platform=platform,
    endpoint_type='login',
    path='/login',
    http_method='POST'
)

# 创建额外配置
PlatformConfig.objects.create(
    platform=platform,
    config_key='login_data_extra',
    config_value={'remember': '1'}
)
```

## 使用方法

### 1. API接口使用

#### 查询认证状态
```bash
GET /api/external-platform/auth-status/city_center_workorder/username/
```

#### 触发登录
```bash
POST /api/external-platform/login/
{
    "platform_sign": "city_center_workorder",
    "account": "username",
    "password": "password"
}
```

#### 查询任务状态
```bash
GET /api/external-platform/task-status/{task_id}/
```

### 2. 编程接口使用

```python
from external_platform.services.auth_service import AuthService

# 获取有效会话
session = AuthService.get_valid_session('city_center_workorder', 'username')

# 触发登录任务
task_id = AuthService.trigger_login_task('city_center_workorder', 'username', 'password')

# 检查会话有效性
is_valid = AuthService.is_session_valid(session)
```

### 3. 管理命令测试

```bash
python manage.py test_external_auth --platform city_center_workorder --account username --password password --create-platform
```

## 数据模型

### 核心模型

1. **Platform** - 外部平台基础信息
   - name: 平台名称
   - sign: 平台标识（唯一）
   - base_url: 基础URL
   - captcha_type: 验证码类型
   - session_timeout_hours: 会话超时时间
   - retry_limit: 重试次数限制
   - is_active: 是否启用

2. **PlatformEndpoint** - 平台端点配置
   - platform: 关联平台
   - endpoint_type: 端点类型（captcha, login, check_status等）
   - name: 端点名称（可选）
   - path: 端点路径
   - http_method: HTTP方法
   - require_auth: 是否需要鉴权

3. **PlatformConfig** - 平台额外配置
   - platform: 关联平台
   - config_key: 配置键
   - config_value: 配置值（JSON格式）

4. **AuthSession** - 认证会话
   - platform: 关联平台
   - account: 账户
   - auth: 认证信息（JSON格式）
   - status: 认证状态
   - expire_time: 过期时间

5. **RequestLog** - 请求日志
   - platform: 关联平台
   - platform_endpoint: 关联平台端点（可选）
   - account: 账户
   - endpoint_path: 端点路径
   - method: HTTP方法
   - status_code: 响应状态码
   - response_time_ms: 响应时间

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Layer     │    │  Service Layer  │    │  Task Layer     │
│                 │    │                 │    │                 │
│ • auth_views    │───▶│ • AuthService   │───▶│ • login_task    │
│ • URL routing   │    │ • CaptchaService│    │ • maintain_task │
│                 │    │ • ExternalClient│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Layer     │    │  External APIs  │    │  Logging        │
│                 │    │                 │    │                 │
│ • Platform      │    │ • 超级鹰API     │    │ • RequestLog    │
│ • AuthSession   │    │ • 工单系统API   │    │ • CaptchaLog    │
│ • RequestLog    │    │                 │    │ • 结构化日志    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 日志说明

### 日志级别
- **INFO**: 关键操作的开始和完成
- **WARNING**: 可恢复的错误和异常情况  
- **ERROR**: 不可恢复的错误和异常
- **DEBUG**: 详细的执行流程和变量值

### 日志示例
```
[2024-01-01 10:00:00] INFO [external_platform.tasks:35] 开始执行登录任务 - 任务ID: abc123, 平台: city_center_workorder, 账户: username
[2024-01-01 10:00:01] INFO [external_platform.services.captcha_service:45] 验证码识别成功 - pic_id: 123456, 识别结果: abcd
[2024-01-01 10:00:02] INFO [external_platform.tasks:180] 登录流程完成 - 任务ID: abc123, 会话ID: 789
```

## 错误处理

### 常见错误及解决方案

1. **验证码识别失败**
   - 检查超级鹰配置和余额
   - 确认验证码类型设置正确

2. **登录失败**
   - 检查用户名密码是否正确
   - 确认目标网站是否可访问

3. **会话过期**
   - 系统会自动清理过期会话
   - 可手动触发刷新任务

4. **任务执行失败**
   - 检查Celery服务是否正常运行
   - 查看详细错误日志

## 性能优化

1. **缓存策略** - 可在Redis中缓存活跃会话
2. **并发控制** - 同一账户避免并发登录
3. **批量处理** - 状态维护任务支持批量处理
4. **监控指标** - 登录成功率、响应时间等

## 安全考虑

1. **敏感信息** - 密码不存储，Cookie加密传输
2. **访问控制** - API需要认证，操作需要权限
3. **日志脱敏** - 敏感字段自动脱敏处理
4. **审计日志** - 完整的操作审计记录

## 扩展说明

### 添加新平台

1. 在Django Admin中创建Platform记录，配置基础信息
2. 添加PlatformEndpoint记录，配置各个端点路径
3. 根据需要添加PlatformConfig记录，配置额外参数
4. 根据需要调整登录逻辑

### 自定义验证码识别

1. 继承`CaptchaService`类
2. 重写`recognize_captcha`方法
3. 在配置中指定自定义服务

### 添加新的认证方式

1. 扩展`ExternalPlatformClient`
2. 添加新的认证方法
3. 更新任务流程

## 故障排查

### 检查清单

1. ✅ Celery服务是否运行
2. ✅ 数据库连接是否正常
3. ✅ 超级鹰配置是否正确
4. ✅ 目标网站是否可访问
5. ✅ 日志级别是否合适

### 常用命令

```bash
# 查看Celery任务状态
celery -A your_project inspect active

# 查看任务历史
celery -A your_project events

# 手动执行维护任务
python manage.py shell -c "from external_platform.tasks import maintain_auth_status_task; maintain_auth_status_task.delay()"

# 查看日志
tail -f logs/external_platform.log
```