from work_order.models import Disposal
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class DisposalSerializer(CustomModelSerializer):
    """
    处置工单 序列化器
    """
    class Meta:
        model = Disposal
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class DisposalFilter(filters.FilterSet):

    class Meta:
        model = Disposal
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'version', 'source_system', 'sync_task_name', 'sync_task_id', 'sync_status', 'external_ps_caption', 'external_record_number', 'external_public_record', 'external_user_id_hide', 'external_co_di_ids', 'external_co_di_ids_hide', 'external_pss_status_attr', 'external_di_ids', 'external_di_ids_hide', 'external_psot_name', 'external_psot_attr', 'external_pso_caption', 'external_note1', 'external_distribute_way', 'external_note8', 'external_note3', 'external_note4', 'external_note5', 'external_note6', 'external_note11', 'external_note', 'external_note10']


class DisposalViewSet(CustomModelViewSet):
    """
    处置工单 视图集
    """
    queryset = Disposal.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = DisposalSerializer
    filterset_class = DisposalFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'disposal', views.DisposalViewSet)
# 移入 __init__.py
# from work_order.views.disposal import DisposalViewSet