from work_order.models import Meta
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class MetaSerializer(CustomModelSerializer):
    """
    原始工单 序列化器
    """
    class Meta:
        model = Meta
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class MetaFilter(filters.FilterSet):

    class Meta:
        model = Meta
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'version', 'source_system', 'sync_task_id', 'sync_status', 'pull_task_id']


class MetaViewSet(CustomModelViewSet):
    """
    原始工单 视图集
    """
    queryset = Meta.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = MetaSerializer
    filterset_class = MetaFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'meta', views.MetaViewSet)
# 移入 __init__.py
# from work_order.views.meta import MetaViewSet