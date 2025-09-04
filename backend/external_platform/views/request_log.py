from external_platform.models import RequestLog
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class RequestLogSerializer(CustomModelSerializer):
    """
    外部系统请求日志 序列化器
    """
    class Meta:
        model = RequestLog
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class RequestLogFilter(filters.FilterSet):

    class Meta:
        model = RequestLog
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'account', 'endpoint_path', 'method', 'status_code', 'response_time_ms']


class RequestLogViewSet(CustomModelViewSet):
    """
    外部系统请求日志 视图集
    """
    queryset = RequestLog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = RequestLogSerializer
    filterset_class = RequestLogFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'request_log', views.RequestLogViewSet)
# 移入 __init__.py
# from external_platform.views.request_log import RequestLogViewSet