import os

# 数据库配置
MYSQL_USER = os.getenv('DB_USER', 'root')
MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'my-secret-pw')
MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
MYSQL_PORT = os.getenv('DB_PORT', '3306')
MYSQL_DB = os.getenv('DB_NAME', 'django_vue')

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
)
