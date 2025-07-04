# syntax=docker/dockerfile:1

####################
# 构建阶段
####################
FROM node:22.17.0 AS build

WORKDIR /app

# 先拷贝依赖文件
COPY package.json ./

# 启用 corepack + 设置 registry
RUN corepack enable \
    && corepack prepare pnpm@latest --activate \
    && pnpm config set registry https://registry.npmjs.org/ \
    && pnpm install

# 再拷贝源码
COPY . .

# 编译
RUN pnpm run build:antd

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

# 拷贝项目
COPY . .

# 如果有私有 registry
COPY .npmrc .npmrc

# 安装 pnpm（官方推荐 corepack，更好）
RUN corepack enable \
 && corepack prepare pnpm@latest --activate

# 安装依赖（一定要在 monorepo 根目录，保证 workspace 有效）
RUN pnpm i

# 设置前端工作目录（根据实际情况修改）
WORKDIR /app/apps/web-antd

# 暴露前端 dev server 端口
EXPOSE 5678

# 默认启动 dev server
CMD ["pnpm", "run", "dev:antd"]
