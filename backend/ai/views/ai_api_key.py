from ai.models import AIApiKey
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class AIApiKeySerializer(CustomModelSerializer):
    """
    AI API 密钥 序列化器
    """
    class Meta:
        model = AIApiKey
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class AIApiKeyViewSet(CustomModelViewSet):
    """
    AI API 密钥 视图集
    """
    queryset = AIApiKey.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AIApiKeySerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'platform', 'api_key', 'url', 'status']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
#
