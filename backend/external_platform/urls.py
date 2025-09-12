from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'request_log', views.RequestLogViewSet)
router.register(r'external_auth_captcha_log', views.ExternalAuthCaptchaLogViewSet)
router.register(r'platform', views.PlatformViewSet)
router.register(r'auth_session', views.AuthSessionViewSet)
router.register(r'platform_endpoint', views.PlatformEndpointViewSet)
router.register(r'platform_config', views.PlatformConfigViewSet)
router.register(r'external_district_node', views.ExternalDistrictNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]