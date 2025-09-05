from external_platform.models import PlatformEndpoint
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class PlatformEndpointSerializer(CustomModelSerializer):
    """
    平台端点配置 序列化器
    """
    class Meta:
        model = PlatformEndpoint
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class PlatformEndpointFilter(filters.FilterSet):

    class Meta:
        model = PlatformEndpoint
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'endpoint_type', 'name', 'path', 'http_method', 'require_auth']


class PlatformEndpointViewSet(CustomModelViewSet):
    """
    平台端点配置 视图集
    """
    queryset = PlatformEndpoint.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PlatformEndpointSerializer
    filterset_class = PlatformEndpointFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'platform_endpoint', views.PlatformEndpointViewSet)
# 移入 __init__.py
# from external_platform.views.platform_endpoint import PlatformEndpointViewSet