from rest_framework import serializers

from ai.models import AIModel
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class AIModelSerializer(CustomModelSerializer):
    api_key_name = serializers.CharField(source='key.name', read_only=True)
    """
    AI 模型 序列化器
    """
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']

class AIModelViewSet(CustomModelViewSet):
    """
    AI 模型 视图集
    """
    queryset = AIModel.objects.filter(is_deleted=False).select_related('key').order_by('-id')
    serializer_class = AIModelSerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'sort', 'status', 'platform',
                        'model', 'max_tokens', 'max_contexts']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

