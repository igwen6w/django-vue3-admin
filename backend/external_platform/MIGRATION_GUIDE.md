# 数据模型迁移指南

## 迁移步骤

### 1. 生成迁移文件

```bash
python manage.py makemigrations external_platform
```

### 2. 执行迁移

```bash
python manage.py migrate external_platform
```

### 3. 初始化配置数据

```bash
python manage.py init_platform_config
```

## 模型变更说明

### Platform 模型扩展
- 添加了 `base_url`, `captcha_type`, `session_timeout_hours`, `retry_limit`, `is_active`, `description` 字段
- `sign` 字段添加了 unique 约束
- `name` 字段长度扩展到 100

### 新增模型
- **PlatformEndpoint**: 管理平台端点配置，替代原有的 ApiEndpoint
- **PlatformConfig**: 管理平台额外配置

### 模型变更
- **移除 ApiEndpoint 模型**: 功能合并到 PlatformEndpoint
- **PlatformEndpoint 扩展**: 添加 `name` 和 `require_auth` 字段

### RequestLog 模型优化
- `endpoint` 字段重命名为 `endpoint_path`
- `api_endpoint` 字段重命名为 `platform_endpoint`，引用 PlatformEndpoint
- 添加了 `account` 字段的索引

## 数据迁移注意事项

1. 如果已有 Platform 数据，需要手动补充新增字段的值
2. 如果已有 RequestLog 数据，`endpoint` 字段会自动重命名为 `endpoint_path`
3. **ApiEndpoint 数据迁移**: 如果有 ApiEndpoint 数据，需要手动迁移到 PlatformEndpoint
4. 建议在迁移前备份数据库

## 配置迁移

原来在 `settings.py` 中的静态配置现在需要迁移到数据库：

```python
# 原配置格式
EXTERNAL_PLATFORMS = {
    'city_center_workorder': {
        'name': '市中心工单系统',
        'base_url': 'https://workorder.citycenter.gov.cn',
        'endpoints': {
            'login': '/login',
            'captcha': '/captcha'
        }
    }
}

# 迁移到数据库后的管理方式
# 1. 在 Django Admin 中创建 Platform 记录
# 2. 创建对应的 PlatformEndpoint 记录
# 3. 如有额外配置，创建 PlatformConfig 记录
```