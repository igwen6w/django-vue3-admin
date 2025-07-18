# syntax=docker/dockerfile:1
FROM python:3.12.2 AS base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
# 入口命令由 docker-compose 控制
# 默认命令，开发和生产通过 docker-compose 覆盖
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS dev

#CMD ["tail", "-f", "/dev/null"]

#CMD ["daphne", "backend.asgi:application"]

# CMD ["sh", "-c", "sleep 5 && python manage.py runserver 0.0.0.0:8000"]


FROM base AS prod

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8010", "--workers", "4"]