from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'ai_api_key', views.AIApiKeyViewSet)
router.register(r'ai_model', views.AIModelViewSet)
router.register(r'tool', views.ToolViewSet)

urlpatterns = [
    path('', include(router.urls)),
]