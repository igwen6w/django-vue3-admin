from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'request_log', views.RequestLogViewSet)
router.register(r'external_auth_captcha_log', views.ExternalAuthCaptchaLogViewSet)
router.register(r'platform', views.PlatformViewSet)
router.register(r'auth_session', views.AuthSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
#     # 认证相关API
#     path('auth-status/<str:platform_sign>/<str:account>/', 
#          auth_views.get_auth_status, name='get_auth_status'),
#     path('login/', auth_views.trigger_login, name='trigger_login'),
#     path('task-status/<str:task_id>/', 
#          auth_views.get_task_status, name='get_task_status'),
#     path('sessions/', auth_views.list_sessions, name='list_sessions'),
#     path('refresh-session/<str:platform_sign>/<str:account>/', 
#          auth_views.refresh_session, name='refresh_session'),
]