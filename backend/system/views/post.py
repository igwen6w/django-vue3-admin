from system.models import Post
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters

class PostSerializer(CustomModelSerializer):
    """
    岗位信息表 序列化器
    """
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class PostFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = Post
        fields = ['name', 'code', 'status']


class PostViewSet(CustomModelViewSet):
    """
    岗位信息表 视图集
    """
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    filterset_class = PostFilter
    search_fields = ['name', 'code']
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']
