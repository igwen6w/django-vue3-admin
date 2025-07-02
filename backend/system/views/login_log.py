from system.models import LoginLog
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from rest_framework import serializers

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


class LoginLogViewSet(CustomModelViewSet):
    """
    系统访问记录 视图集
    """
    queryset = LoginLog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = LoginLogSerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'username', 'result', 'user_ip', 'user_agent']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
