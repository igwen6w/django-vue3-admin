from system.models import Post
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class PostSerializer(CustomModelSerializer):
    """
    岗位信息表 序列化器
    """
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class PostViewSet(CustomModelViewSet):
    """
    岗位信息表 视图集
    """
    queryset = Post.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PostSerializer
    filterset_fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'code', 'name', 'sort', 'status']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
