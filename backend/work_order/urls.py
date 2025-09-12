from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'demo', views.DemoViewSet)
router.register(r'meta', views.MetaViewSet)
router.register(r'disposal', views.DisposalViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'base', views.BaseViewSet)


urlpatterns = [
    path('', include(router.urls)),
]