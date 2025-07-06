---
sidebar_position: 6
---
# Docker 启动

1. 安装 Docker 与 Docker Compose
2. 在项目根目录执行：

```bash
cp docker/.env.example docker/.env.local
# 根据实际情况修改 docker/.env.local
docker-compose -f docker-compose.dev.yml up -d
```

3. 访问前后端服务地址，默认端口可在 compose 文件中查看和修改。 