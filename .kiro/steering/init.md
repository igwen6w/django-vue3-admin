---
inclusion: always
---

# 项目开发指南

## 项目架构
- **后端**: Django REST Framework (DRF) 代码位于 `backend/` 文件夹中
- **前端**: Vue.js 应用位于 `web/` 文件夹中  
- **AI服务**: FastAPI 微服务位于 `ai_service/` 文件夹中
- **文档**: 项目文档位于 `docs/` 文件夹中

## 语言规范
- **对话语言**: 优先使用中文进行交流和说明
- **代码注释**: 使用中文编写注释和文档字符串
- **文档编写**: 技术文档和README文件优先使用中文

## 代码规范
- **Python**: 遵循PEP 8规范，使用Django和DRF最佳实践
- **JavaScript/TypeScript**: 遵循项目中的ESLint配置
- **数据库**: 使用Django ORM进行数据库操作
- **API设计**: 遵循RESTful API设计原则

## 开发约定
- 新功能开发前先查看相关的Django应用结构
- 数据库迁移文件需要妥善管理
- 外部平台集成代码位于 `external_platform/` 应用中
- AI相关功能集成在 `ai/` 应用和 `ai_service/` 微服务中