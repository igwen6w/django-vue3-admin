from work_order.models import Category
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class CategorySerializer(CustomModelSerializer):
    """
    工单分类 序列化器
    """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class CategoryFilter(filters.FilterSet):

    class Meta:
        model = Category
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name']


class CategoryViewSet(CustomModelViewSet):
    """
    工单分类 视图集
    """
    queryset = Category.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'category', views.CategoryViewSet)
# 移入 __init__.py
# from work_order.views.category import CategoryViewSet