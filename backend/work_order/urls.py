from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'demo', views.DemoViewSet)
router.register(r'meta', views.MetaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]