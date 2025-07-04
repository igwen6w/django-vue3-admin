# syntax=docker/dockerfile:1
####################
# 生产阶段
####################
FROM nginx:alpine AS prod

# 拷贝编译后的静态文件到 nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 拷贝 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf


####################
# 开发阶段
####################
FROM node:22.17.0 AS dev

WORKDIR /app

ENV PNPM_SKIP_PROMPT=true

# 拷贝项目
COPY . .

COPY /apps/web-antd/.env.docker /apps/web-antd/.env.local

# 安装 pnpm（官方推荐 corepack，更好）
RUN corepack enable && corepack prepare pnpm@latest --activate

# 安装依赖（一定要在 monorepo 根目录，保证 workspace 有效）
RUN pnpm store prune && rm -rf $(pnpm store path) && \
    rm -rf node_modules .npmrc package-lock.json pnpm-lock.yaml .pnpm-store .turbo && \
    find . -name 'node_modules' -type d -prune -exec rm -rf '{}' +

RUN npm run clean

RUN yes | pnpm recursive install

# 设置前端工作目录（根据实际情况修改）
# 暴露前端 dev server 端口
EXPOSE 5678
#CMD ["tail", "-f", "/dev/null"]

# 默认启动 dev server
CMD ["npm", "run", "dev:antd"]
