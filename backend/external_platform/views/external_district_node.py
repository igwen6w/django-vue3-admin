from external_platform.models import ExternalDistrictNode
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from collections import defaultdict


class ExternalDistrictNodeSerializer(CustomModelSerializer):
    """
    区县节点 序列化器
    """
    class Meta:
        model = ExternalDistrictNode
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ExternalDistrictNodeFilter(filters.FilterSet):

    class Meta:
        model = ExternalDistrictNode
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'code']


class ExternalDistrictNodeViewSet(CustomModelViewSet):
    """
    区县节点 视图集
    """
    queryset = ExternalDistrictNode.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalDistrictNodeSerializer
    filterset_class = ExternalDistrictNodeFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

    @action(detail=False, methods=['get'])
    def tree(self, request):
        all_district_nodes = ExternalDistrictNode.objects.all().order_by('-id')
        district_node_dict = {}
        children_map = defaultdict(list)
        for district_node in all_district_nodes:
            item = {
                'id': district_node.id,
                'parent': district_node.parent_id,
                'name': district_node.name,
                'code': district_node.code,
                'children': [],
            }
            district_node_dict[district_node.id] = item
            if district_node.parent_id:
                children_map[district_node.parent_id].append(item)
            
            for district_node_id, district_node in district_node_dict.items():
                district_node['children'] = children_map.get(district_node_id, [])
                
        tree = [district_node for district_node in district_node_dict.values() if district_node['parent'] is None]
        return self._build_response(
            data=tree,
            message="ok",
            status=status.HTTP_200_OK,
        )


# 移入urls中
# router.register(r'external_district_node', views.ExternalDistrictNodeViewSet)
# 移入 __init__.py
# from external_platform.views.external_district_node import ExternalDistrictNodeViewSet