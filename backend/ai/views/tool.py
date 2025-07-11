from ai.models import Tool
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class ToolSerializer(CustomModelSerializer):
    """
    AI 工具 序列化器
    """
    class Meta:
        model = Tool
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ToolViewSet(CustomModelViewSet):
    """
    AI 工具 视图集
    """
    queryset = Tool.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ToolSerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'description', 'status']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
