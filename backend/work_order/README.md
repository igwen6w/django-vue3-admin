# 工单同步系统使用指南

## 概述

这是一个基于 Django + Celery 的工单同步系统，可以从外部工单系统（如 Jira、Zendesk 等）自动拉取工单数据，并提供统一的工单管理界面。

## 架构设计

### 核心组件

1. **数据模型** (`models.py`)
   - `WorkOrderSystem`: 外部工单系统配置
   - `WorkOrder`: 工单数据模型
   - `WorkOrderSyncLog`: 同步日志

2. **适配器层** (`adapters.py`)
   - `BaseWorkOrderAdapter`: 适配器基类
   - `JiraAdapter`: Jira 系统适配器
   - `ZendeskAdapter`: Zendesk 系统适配器
   - `WorkOrderAdapterFactory`: 适配器工厂

3. **服务层** (`services.py`)
   - `WorkOrderSyncService`: 工单同步服务
   - `WorkOrderSyncManager`: 同步管理器

4. **任务层** (`tasks.py`)
   - Celery 异步任务定义
   - 定时任务配置

5. **API 层** (`views/`)
   - `WorkOrderSystemViewSet`: 系统配置管理
   - `WorkOrderViewSet`: 工单数据管理
   - `WorkOrderSyncLogViewSet`: 同步日志管理

## 快速开始

### 1. 数据库迁移

```bash
python manage.py makemigrations work_order
python manage.py migrate
```

### 2. 启动 Celery

```bash
# 启动 Celery Worker
celery -A backend worker -l info

# 启动 Celery Beat（定时任务）
celery -A backend beat -l info
```

### 3. 配置外部工单系统

#### 通过 Django Admin 配置

1. 访问 Django Admin 界面
2. 进入 "工单系统配置" 模块
3. 添加新的工单系统配置

#### 通过 API 配置

```bash
# 创建 Jira 系统配置
curl -X POST http://localhost:8000/api/work-order-systems/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "jira",
    "api_url": "https://your-jira-instance.com",
    "api_key": "your-api-key",
    "username": "your-username",
    "password": "your-password",
    "is_active": true,
    "sync_interval": 300
  }'
```

### 4. 手动同步工单

#### 使用管理命令

```bash
# 同步所有系统
python manage.py sync_work_orders --all

# 同步指定系统
python manage.py sync_work_orders --system-id 1

# 查看同步状态
python manage.py sync_work_orders --status

# 清理旧日志
python manage.py sync_work_orders --clean-logs --days 30
```

#### 使用 API

```bash
# 同步所有系统
curl -X POST http://localhost:8000/api/work-order-systems/sync_all/

# 同步指定系统
curl -X POST http://localhost:8000/api/work-order-systems/1/sync/

# 测试连接
curl -X POST http://localhost:8000/api/work-order-systems/1/test_connection/
```

## API 接口

### 工单系统配置

- `GET /api/work-order-systems/` - 获取系统配置列表
- `POST /api/work-order-systems/` - 创建系统配置
- `GET /api/work-order-systems/{id}/` - 获取系统配置详情
- `PUT /api/work-order-systems/{id}/` - 更新系统配置
- `DELETE /api/work-order-systems/{id}/` - 删除系统配置
- `POST /api/work-order-systems/{id}/sync/` - 同步指定系统
- `POST /api/work-order-systems/sync_all/` - 同步所有系统
- `POST /api/work-order-systems/{id}/test_connection/` - 测试连接
- `POST /api/work-order-systems/{id}/enable/` - 启用系统
- `POST /api/work-order-systems/{id}/disable/` - 禁用系统

### 工单数据

- `GET /api/work-orders/` - 获取工单列表
- `GET /api/work-orders/{id}/` - 获取工单详情
- `PUT /api/work-orders/{id}/` - 更新工单
- `GET /api/work-orders/statistics/` - 获取统计信息
- `GET /api/work-orders/overdue/` - 获取逾期工单
- `GET /api/work-orders/upcoming_deadline/` - 获取即将到期工单
- `POST /api/work-orders/{id}/update_external/` - 更新外部系统工单

### 同步日志

- `GET /api/sync-logs/` - 获取同步日志列表
- `GET /api/sync-logs/{id}/` - 获取同步日志详情
- `GET /api/sync-logs/statistics/` - 获取日志统计信息
- `GET /api/sync-logs/recent_failures/` - 获取最近失败日志
- `GET /api/sync-logs/performance_analysis/` - 性能分析

## 定时任务配置

系统默认配置了以下定时任务：

- **工单同步**: 每5分钟执行一次
- **日志清理**: 每24小时执行一次

可以在 `settings.py` 中修改 `CELERY_BEAT_SCHEDULE` 配置：

```python
CELERY_BEAT_SCHEDULE = {
    'sync-work-orders-every-5-minutes': {
        'task': 'work_order.tasks.sync_work_order_data',
        'schedule': 300,  # 5分钟
    },
    'clean-sync-logs-daily': {
        'task': 'work_order.tasks.clean_old_sync_logs',
        'schedule': 86400,  # 24小时
    },
}
```

## 扩展新的工单系统

### 1. 创建适配器

继承 `BaseWorkOrderAdapter` 类：

```python
class CustomAdapter(BaseWorkOrderAdapter):
    def authenticate(self) -> bool:
        # 实现认证逻辑
        pass
    
    def get_work_orders(self, since=None, limit=100):
        # 实现获取工单列表逻辑
        pass
    
    def get_work_order_detail(self, external_id):
        # 实现获取工单详情逻辑
        pass
    
    def update_work_order(self, external_id, data):
        # 实现更新工单逻辑
        pass
```

### 2. 注册适配器

在 `WorkOrderAdapterFactory` 中注册：

```python
ADAPTERS = {
    'jira': JiraAdapter,
    'zendesk': ZendeskAdapter,
    'custom': CustomAdapter,  # 添加新适配器
}
```

## 监控和日志

### 日志配置

系统使用 Django 的日志系统，可以在 `settings.py` 中配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'work_order_sync.log',
        },
    },
    'loggers': {
        'work_order': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 监控指标

系统提供以下监控指标：

- 同步成功率
- 平均执行时间
- 失败次数统计
- 各系统性能对比

## 故障排除

### 常见问题

1. **认证失败**
   - 检查 API 密钥和用户名密码
   - 确认外部系统 API 地址正确
   - 验证网络连接

2. **同步失败**
   - 查看同步日志详情
   - 检查外部系统 API 限制
   - 验证数据格式

3. **定时任务不执行**
   - 确认 Celery Beat 已启动
   - 检查 Redis 连接
   - 查看 Celery 日志

### 调试命令

```bash
# 查看 Celery 任务状态
celery -A backend inspect active

# 查看定时任务
celery -A backend inspect scheduled

# 查看任务结果
celery -A backend inspect stats
```

## 性能优化

1. **数据库优化**
   - 为常用查询字段添加索引
   - 使用 `select_related` 减少查询次数
   - 定期清理旧数据

2. **同步优化**
   - 调整同步间隔
   - 使用增量同步
   - 批量处理数据

3. **缓存优化**
   - 缓存外部系统认证信息
   - 缓存统计查询结果
   - 使用 Redis 缓存

## 安全考虑

1. **敏感信息保护**
   - API 密钥和密码字段已设置为 `write_only`
   - 在管理界面中隐藏敏感信息
   - 使用环境变量存储敏感配置

2. **访问控制**
   - 实现适当的权限控制
   - 限制 API 访问频率
   - 记录操作日志

3. **数据验证**
   - 验证外部系统数据格式
   - 防止 SQL 注入
   - 输入数据清理

## 贡献指南

1. 遵循 PEP 8 代码规范
2. 添加适当的文档字符串
3. 编写单元测试
4. 提交前运行测试套件

## 许可证

本项目采用 MIT 许可证。
