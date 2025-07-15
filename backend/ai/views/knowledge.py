from ai.models import Knowledge
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class KnowledgeSerializer(CustomModelSerializer):
    """
    AI 知识库 序列化器
    """
    class Meta:
        model = Knowledge
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class KnowledgeViewSet(CustomModelViewSet):
    """
    AI 知识库 视图集
    """
    queryset = Knowledge.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = KnowledgeSerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'embedding_model', 'top_k', 'status']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
