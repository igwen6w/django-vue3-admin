"""
网关API URL配置
"""
from django.urls import path, include
from . import views

app_name = 'gateway'

urlpatterns = [

    # 文件操作
    path('file/upload/', views.upload_file, name='upload_file'),
]
