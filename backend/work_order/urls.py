from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'demo', views.DemoViewSet)
router.register(r'meta', views.MetaViewSet)
router.register(r'disposal', views.DisposalViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'base', views.BaseViewSet)
router.register(r'distribute_opinion_preset', views.DistributeOpinionPresetViewSet)
router.register(r'distribute', views.DistributeViewSet)
router.register(r'supervise', views.SuperviseViewSet)


urlpatterns = [
    path('', include(router.urls)),
]