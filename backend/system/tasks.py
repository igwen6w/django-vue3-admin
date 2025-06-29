# 某个 app 目录下的 tasks.py
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def sync_temu_order():
    pass

@shared_task
def sync_temu_shipping():
    pass