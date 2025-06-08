# 使用官方 Node 镜像作为构建阶段
FROM node:20-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目所有文件
COPY . .

# 构建 Vite 项目
RUN npm run build

# 生产镜像阶段
FROM nginx:stable-alpine AS production

# 复制构建好的静态文件到 nginx 默认目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 替换默认 nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口 7005
EXPOSE 7005

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
