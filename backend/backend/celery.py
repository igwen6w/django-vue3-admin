import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # 请将 myproject 替换为你的项目名称
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Windows 兼容性设置
if os.name == 'nt':
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],  # Ignore other content
        result_serializer='json',
        timezone='Asia/Shanghai',
        enable_utc=True,
    )
    # 强制使用 single-threaded 执行模式
    app.conf.worker_pool = 'solo'