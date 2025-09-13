from work_order.models import BaseEditRecord
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters
from rest_framework.views import APIView


class BaseEditRecordSerializer(CustomModelSerializer):
    """
    工单表编辑记录 序列化器
    """
    class Meta:
        model = BaseEditRecord
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class BaseEditRecordFilter(filters.FilterSet):

    class Meta:
        model = BaseEditRecord
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'external_id', 'act', 'external_payroll_result', 'external_roll_number', 'external_product_ids', 'external_addr2', 'external_company_address', 'external_order_number', 'external_note16', 'sync_task_id', 'sync_status']


class BaseEditRecordViewSet(CustomModelViewSet):
    """
    工单表编辑记录 视图集
    """
    queryset = BaseEditRecord.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BaseEditRecordSerializer
    filterset_class = BaseEditRecordFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
        



# 移入urls中
# router.register(r'base_edit_record', views.BaseEditRecordViewSet)
# 移入 __init__.py
# from work_order.views.base_edit_record import BaseEditRecordViewSet

