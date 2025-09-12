from work_order.models import DistributeOpinionPreset
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class DistributeOpinionPresetSerializer(CustomModelSerializer):
    """
    下派意见预设 序列化器
    """
    class Meta:
        model = DistributeOpinionPreset
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class DistributeOpinionPresetFilter(filters.FilterSet):

    class Meta:
        model = DistributeOpinionPreset
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'title']


class DistributeOpinionPresetViewSet(CustomModelViewSet):
    """
    下派意见预设 视图集
    """
    queryset = DistributeOpinionPreset.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = DistributeOpinionPresetSerializer
    filterset_class = DistributeOpinionPresetFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'distribute_opinion_preset', views.DistributeOpinionPresetViewSet)
# 移入 __init__.py
# from work_order.views.distribute_opinion_preset import DistributeOpinionPresetViewSet