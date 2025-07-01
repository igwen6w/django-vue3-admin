# CRUD 代码生成器

这是一个 Django 管理命令，用于根据模型自动生成完整的 CRUD 代码，包括后端 API 和前端页面。

## 使用方法

### 基本用法

```bash
# 只生成后端代码
python manage.py generate_crud <app_name> <model_name>

# 同时生成前端和后端代码
python manage.py generate_crud <app_name> <model_name> --frontend
```

### 示例

```bash
# 为 system 应用的 Dept 模型生成 CRUD 代码
python manage.py generate_crud system Dept --frontend
```

## 生成的文件

### 后端文件

1. **序列化器**: `backend/{app_name}/serializers.py`
   - 继承 `CustomModelSerializer`
   - 自动处理 creator 和 modifier 字段

2. **视图集**: `backend/{app_name}/views/{model_name.lower()}.py`
   - 继承 `CustomModelViewSet`
   - 包含基本的 CRUD 操作
   - 自动配置过滤、搜索、排序字段

### 前端文件（使用 --frontend 参数时）

1. **模型定义**: `web/apps/web-antd/src/models/{app_name.lower()}.ts`
   - TypeScript 接口定义
   - 继承 BaseModel

2. **API 接口**: `web/apps/web-antd/src/api/{app_name.lower()}/{model_name.lower()}.ts`
   - 完整的 CRUD API 函数
   - TypeScript 类型定义

3. **列表页面**: `web/apps/web-antd/src/views/{app_name.lower()}/{model_name.lower()}/list.vue`
   - 使用 VxeTable 的列表页面
   - 包含增删改查操作

4. **表单配置**: `web/apps/web-antd/src/views/{app_name.lower()}/{model_name.lower()}/data.ts`
   - 表单字段配置
   - 表格列配置

5. **表单组件**: `web/apps/web-antd/src/views/{app_name.lower()}/{model_name.lower()}/modules/form.vue`
   - 可复用的表单组件
   - 支持创建和编辑

## 特性

- **自动字段映射**: 根据 Django 模型字段自动生成对应的前端表单字段
- **类型安全**: 自动生成 TypeScript 类型定义
- **审计字段**: 自动处理 creator、modifier 等审计字段
- **软删除**: 自动过滤已删除的记录
- **分页支持**: 自动配置分页功能
- **搜索过滤**: 自动配置搜索和过滤字段

## 注意事项

1. 确保模型继承自 `CoreModel` 以获得审计字段支持
2. 前端代码需要根据实际需求进行调整
3. 路由配置需要手动添加到 Django 的 URL 配置中
4. 前端路由需要手动配置

## 自定义

你可以根据需要修改生成器代码来：

- 调整生成的代码模板
- 添加更多字段类型支持
- 自定义表单验证规则
- 添加更多前端组件支持 