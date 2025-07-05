# syntax=docker/dockerfile:1
FROM python:3.12.2 AS base

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
# 入口命令由 docker-compose 控制
# 收集静态文件
RUN python manage.py collectstatic --noinput


# 默认命令，开发和生产通过 docker-compose 覆盖
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS dev

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# CMD ["sh", "-c", "sleep 5 && python manage.py runserver 0.0.0.0:8000"]


FROM base AS prod

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
