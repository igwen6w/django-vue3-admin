"""
工单模块 URL 配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.work_order_system import WorkOrderSystemViewSet
from .views.work_order import WorkOrderViewSet
from .views.sync_log import WorkOrderSyncLogViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'work-order-systems', WorkOrderSystemViewSet, basename='work-order-system')
router.register(r'work-orders', WorkOrderViewSet, basename='work-order')
router.register(r'sync-logs', WorkOrderSyncLogViewSet, basename='sync-log')

urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
]