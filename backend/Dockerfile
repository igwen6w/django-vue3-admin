# syntax=docker/dockerfile:1
FROM python:3.12.2

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# 默认命令，开发和生产通过 docker-compose 覆盖
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 