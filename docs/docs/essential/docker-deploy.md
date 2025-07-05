---
sidebar_position: 7
---
# Docker 项目部署（生产环境）

1. 配置生产环境变量和数据库
2. 构建前端静态文件并拷贝到后端 static 目录
3. 执行：

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

4. 检查服务状态，确保一切正常。 