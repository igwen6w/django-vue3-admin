from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'demo', views.DemoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]