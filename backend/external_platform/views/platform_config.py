from external_platform.models import PlatformConfig
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class PlatformConfigSerializer(CustomModelSerializer):
    """
    平台配置 序列化器
    """
    class Meta:
        model = PlatformConfig
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class PlatformConfigFilter(filters.FilterSet):

    class Meta:
        model = PlatformConfig
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'config_key']


class PlatformConfigViewSet(CustomModelViewSet):
    """
    平台配置 视图集
    """
    queryset = PlatformConfig.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PlatformConfigSerializer
    filterset_class = PlatformConfigFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'platform_config', views.PlatformConfigViewSet)
# 移入 __init__.py
# from external_platform.views.platform_config import PlatformConfigViewSet