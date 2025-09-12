from work_order.models import Base
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class BaseSerializer(CustomModelSerializer):
    """
    工单表 序列化器
    """
    class Meta:
        model = Base
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class BaseFilter(filters.FilterSet):

    class Meta:
        model = Base
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'version', 'source_system', 'sync_task_name', 'sync_task_id', 'sync_status', 'external_id', 'external_roll_number', 'external_handle_rel_expire_time', 'external_src_way', 'external_payroll_name', 'external_company_tel', 'external_addr', 'external_region_district_id', 'external_note14', 'external_distribute_way', 'external_payroll_type', 'external_event_type2_id', 'external_product_ids', 'external_addr2', 'external_company_address', 'external_order_number', 'external_addr3', 'external_note1', 'external_note4', 'external_handling_quality', 'external_note12', 'external_note2', 'external_note3', 'external_note16', 'current_node']


class BaseViewSet(CustomModelViewSet):
    """
    工单表 视图集
    """
    queryset = Base.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BaseSerializer
    filterset_class = BaseFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'base', views.BaseViewSet)
# 移入 __init__.py
# from work_order.views.base import BaseViewSet