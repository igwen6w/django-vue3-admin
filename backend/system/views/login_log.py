from system.models import LoginLog
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from rest_framework import serializers
from utils.permissions import HasButtonPermission
from django_filters import rest_framework as filters

class LoginLogSerializer(CustomModelSerializer):
    """
    系统访问记录 序列化器
    """
    result_text = serializers.SerializerMethodField()

    class Meta:
        model = LoginLog
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']

    def get_result_text(self, obj):
        return obj.get_result_display()


class LoginLogFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    create_time = filters.DateFromToRangeFilter(field_name='create_time')

    class Meta:
        model = LoginLog
        fields = ['username', 'create_time']


class LoginLogViewSet(CustomModelViewSet):
    """
    系统访问记录 视图集
    """
    queryset = LoginLog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = LoginLogSerializer
    filterset_class = LoginLogFilter
    search_fields = ['username']
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
    permission_classes = [HasButtonPermission]
