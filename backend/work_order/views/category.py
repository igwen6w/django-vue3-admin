from collections import defaultdict
from work_order.models import Category
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.decorators import action


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

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取工单分类树形结构"""
        all_categories = Category.objects.all().order_by('-id')
        category_dict = {}
        children_map = defaultdict(list)
        for category in all_categories:
            item = {
                'id': category.id,
                'parent': category.parent_id,
                'name': category.name,
                'description': category.description,
                'children': [],
            }
            category_dict[category.id] = item
            if category.parent_id:
                children_map[category.parent_id].append(item)
            
            for category_id, category in category_dict.items():
                category['children'] = children_map.get(category_id, [])
                
        tree = [category for category in category_dict.values() if category['parent'] is None]
        return self._build_response(
            data=tree,
            message="ok",
            status=status.HTTP_200_OK,
        )

# 移入urls中
# router.register(r'category', views.CategoryViewSet)
# 移入 __init__.py
# from work_order.views.category import CategoryViewSet