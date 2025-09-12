from work_order.models import Distribute
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class DistributeSerializer(CustomModelSerializer):
    """
    下派工单 序列化器
    """
    class Meta:
        model = Distribute
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class DistributeFilter(filters.FilterSet):

    class Meta:
        model = Distribute
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'external_ps_caption', 'external_record_number', 'external_public_record', 'external_user_id_hide', 'external_pss_status_attr', 'external_psot_name', 'external_psot_attr', 'external_pso_caption', 'external_dept_send_msg', 'external_note', 'external_expires']


class DistributeViewSet(CustomModelViewSet):
    """
    下派工单 视图集
    """
    queryset = Distribute.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = DistributeSerializer
    filterset_class = DistributeFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'distribute', views.DistributeViewSet)
# 移入 __init__.py
# from work_order.views.distribute import DistributeViewSet