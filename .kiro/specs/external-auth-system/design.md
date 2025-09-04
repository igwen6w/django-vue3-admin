# 设计文档

## 系统架构概述

本系统采用基于Celery异步任务的外部平台认证管理架构，主要包含以下核心组件：

1. **认证服务层** - 提供统一的认证接口
2. **异步任务层** - 处理登录和状态维护的Celery任务
3. **验证码识别服务** - 集成超级鹰平台的验证码识别
4. **数据持久化层** - 管理认证会话和日志数据
5. **API端点管理** - 动态配置外部平台接口

## 核心组件设计

### 1. 认证服务 (AuthService)

**职责：** 提供统一的认证状态管理接口

**主要方法：**
- `get_valid_session(platform_sign, account)` - 获取有效认证会话
- `trigger_login_task(platform_sign, account)` - 触发异步登录任务
- `check_session_validity(session)` - 检查会话有效性

### 2. Celery异步任务

#### 2.1 登录任务 (login_task)
```python
@shared_task(bind=True, max_retries=3)
def login_task(self, platform_sign: str, account: str, password: str)
```

**流程：**
1. 获取验证码图片和初始Cookie
2. 调用超级鹰识别验证码
3. 提交登录请求
4. 保存认证会话到数据库
5. 记录请求日志

#### 2.2 状态维护任务 (maintain_auth_status_task)
```python
@periodic_task(run_every=crontab(minute='*/10'))
def maintain_auth_status_task()
```

**流程：**
1. 查询所有活跃的认证会话
2. 检查会话是否接近过期
3. 对即将过期的会话触发刷新
4. 更新过期会话状态为EXPIRED

### 3. 验证码识别服务 (CaptchaService)

**基于超级鹰平台的验证码识别服务**

```python
class CaptchaService:
    def __init__(self, username: str, password: str, software_id: str)
    def recognize_captcha(self, image_data: bytes, captcha_type: int) -> dict
    def report_error(self, pic_id: str) -> dict
```

### 4. 外部平台客户端 (ExternalPlatformClient)

**职责：** 封装与外部平台的HTTP交互

**主要方法：**
- `get_captcha()` - 获取验证码图片
- `login(username, password, captcha, cookies)` - 执行登录
- `check_login_status(cookies)` - 检查登录状态
- `make_authenticated_request()` - 发送认证请求

## 数据流设计

### 登录流程数据流

```
1. API调用 -> AuthService.get_valid_session()
2. 检查本地会话 -> 如果无效 -> 触发login_task
3. login_task -> 获取验证码 -> CaptchaService.recognize_captcha()
4. login_task -> 提交登录 -> ExternalPlatformClient.login()
5. login_task -> 保存会话 -> AuthSession.save()
6. login_task -> 记录日志 -> RequestLog.create()
```

### 状态维护数据流

```
1. 定时任务 -> maintain_auth_status_task()
2. 查询活跃会话 -> AuthSession.objects.filter(status='active')
3. 检查过期时间 -> 触发刷新或标记过期
4. 更新会话状态 -> AuthSession.save()
```

## API设计

### 认证接口

```python
# 获取认证状态
GET /api/external-platform/auth-status/{platform_sign}/{account}/

# 触发登录任务
POST /api/external-platform/login/
{
    "platform_sign": "city_center_workorder",
    "account": "username",
    "password": "password"
}

# 查询任务状态
GET /api/external-platform/task-status/{task_id}/
```

## 错误处理设计

### 错误分类

1. **网络错误** - 连接超时、DNS解析失败
2. **认证错误** - 用户名密码错误、验证码错误
3. **验证码识别错误** - 超级鹰识别失败
4. **系统错误** - 数据库连接失败、配置错误

### 重试策略

- **登录任务重试：** 最大3次，指数退避
- **验证码识别重试：** 最大2次，立即重试
- **网络请求重试：** 最大3次，固定间隔

## 日志设计

### 日志级别

- **DEBUG：** 详细的执行流程和变量值
- **INFO：** 关键操作的开始和完成
- **WARNING：** 可恢复的错误和异常情况
- **ERROR：** 不可恢复的错误和异常

### 日志内容

```python
# 登录开始
logger.info(f"开始登录任务 - 平台: {platform_sign}, 账户: {account}, 任务ID: {task_id}")

# 验证码识别
logger.info(f"验证码识别成功 - 平台: {platform_sign}, 识别结果: {captcha_result}, 耗时: {duration}ms")

# 登录成功
logger.info(f"登录成功 - 平台: {platform_sign}, 账户: {account}, 会话ID: {session_id}")

# 错误日志
logger.error(f"登录失败 - 平台: {platform_sign}, 账户: {account}, 错误: {error_msg}", exc_info=True)
```

## 配置设计

### 平台配置

```python
EXTERNAL_PLATFORMS = {
    'city_center_workorder': {
        'name': '市中心工单系统',
        'base_url': 'https://workorder.citycenter.gov.cn',
        'captcha_type': 1004,  # 超级鹰验证码类型
        'session_timeout': 3600,  # 会话超时时间(秒)
        'retry_limit': 3,
        'endpoints': {
            'captcha': '/captcha',
            'login': '/login',
            'check_status': '/user/info'
        }
    }
}
```

### 超级鹰配置

```python
CHAOJIYING_CONFIG = {
    'username': 'your_username',
    'password': 'your_password', 
    'software_id': 'your_software_id',
    'timeout': 30
}
```

## 性能考虑

### 缓存策略

- **会话缓存：** Redis缓存活跃会话，减少数据库查询
- **配置缓存：** 内存缓存平台配置，避免重复读取

### 并发控制

- **登录任务：** 同一账户同时只能有一个登录任务
- **状态检查：** 使用分布式锁避免重复检查

### 监控指标

- 登录成功率
- 验证码识别成功率
- 平均登录耗时
- 会话有效期分布

## 安全考虑

### 敏感信息保护

- 密码加密存储
- Cookie安全传输
- 日志脱敏处理

### 访问控制

- API接口权限验证
- 任务执行权限控制
- 敏感操作审计日志