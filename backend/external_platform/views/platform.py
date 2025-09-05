from external_platform.models import Platform
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class PlatformSerializer(CustomModelSerializer):
    """
    外部平台 序列化器
    """
    class Meta:
        model = Platform
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class PlatformFilter(filters.FilterSet):

    class Meta:
        model = Platform
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'sign', 'base_url', 'captcha_type', 'session_timeout_hours', 'retry_limit', 'is_active']


class PlatformViewSet(CustomModelViewSet):
    """
    外部平台 视图集
    """
    queryset = Platform.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PlatformSerializer
    filterset_class = PlatformFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'platform', views.PlatformViewSet)
# 移入 __init__.py
# from external_platform.views.platform import PlatformViewSet