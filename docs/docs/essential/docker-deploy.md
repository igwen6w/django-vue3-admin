---
sidebar_position: 7
---
# Docker 项目部署（生产环境）

```bash
# 配置生产环境变量和数据库 根据实际情况修改 docker/.env.local
cp docker/.env.example docker/.env.local

# 可选(阿里oss)
# vim web/apps/web-antd/.env.production.local
# 添加以下内容, 按实际值填
# VITE_OSS_ENABLED=true
# VITE_OSS_REGION=
# VITE_OSS_ACCESS_KEY_ID=
# VITE_OSS_ACCESS_KEY_SECRET=
# VITE_OSS_BUCKET=
# VITE_OSS_PREFIX=
# VITE_OSS_DELETE_LOCAL=


# 执行
docker-compose -f docker-compose.prod.yml up -d --build
```

4. 检查服务状态，确保一切正常。 