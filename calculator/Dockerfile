# 使用官方 Python 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将依赖文件复制到容器中
COPY requirements.txt .

# 设置为清华源
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将项目文件复制到容器中
COPY . .

# 暴露容器端口
EXPOSE 5000

# 启动 Flask 应用，使用 Gunicorn
# 替换 app:app 中的 app 是 Python 文件名，后面的 app 是 Flask 实例名
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
