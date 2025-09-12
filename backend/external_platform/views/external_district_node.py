from external_platform.models import ExternalDistrictNode
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class ExternalDistrictNodeSerializer(CustomModelSerializer):
    """
    区县节点 序列化器
    """
    class Meta:
        model = ExternalDistrictNode
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ExternalDistrictNodeFilter(filters.FilterSet):

    class Meta:
        model = ExternalDistrictNode
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'code']


class ExternalDistrictNodeViewSet(CustomModelViewSet):
    """
    区县节点 视图集
    """
    queryset = ExternalDistrictNode.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalDistrictNodeSerializer
    filterset_class = ExternalDistrictNodeFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'external_district_node', views.ExternalDistrictNodeViewSet)
# 移入 __init__.py
# from external_platform.views.external_district_node import ExternalDistrictNodeViewSet