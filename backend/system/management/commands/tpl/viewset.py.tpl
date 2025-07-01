from $app_name.models import $model_name
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet

class ${model_name}Serializer(CustomModelSerializer):
    """
    $verbose_name 序列化器
    """
    class Meta:
        model = $model_name
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ${model_name}ViewSet(CustomModelViewSet):
    """
    $verbose_name 视图集
    """
    queryset = $model_name.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ${model_name}Serializer
    filterset_fields = [$filterset_fields]
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'${model_name_snake}', views.${model_name}ViewSet)
