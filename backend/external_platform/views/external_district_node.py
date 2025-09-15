from external_platform.models import ExternalDistrictNode
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from collections import defaultdict
from django.db import connection


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
        all_district_nodes = ExternalDistrictNode.objects.all().order_by('code')
        district_node_dict = {}
        children_map = defaultdict(list)
        for district_node in all_district_nodes:
            item = {
                'parent': district_node.parent_id,
                'name': district_node.name,
                'code': district_node.code,
                'children': [],
            }
            district_node_dict[district_node.code] = item
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
    

    @action(detail=False, methods=['get'])
    def tree_from_parent(self, request):
        """从选中的父级区县节点，构建树形结构"""
        parent = request.query_params.get('parent')

        from distutils.util import strtobool

        try:
            show_parent = bool(strtobool(request.query_params.get('show_parent', '0')))
        except ValueError:
            show_parent = False  # 无效值时的默认值
    
        if not parent:
            return self._build_response(
                data=[],
                message="parent 参数不能为空",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # 使用递归CTE一次性查询所有子孙节点
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH RECURSIVE district_tree AS (
                    -- 基础查询：直接子节点
                    SELECT code, name, parent_id, 1 as level
                    FROM external_district_node 
                    WHERE parent_id = %s
                    
                    UNION ALL
                    
                    -- 递归查询：子节点的子节点
                    SELECT e.code, e.name, e.parent_id, dt.level + 1
                    FROM external_district_node e
                    INNER JOIN district_tree dt ON e.parent_id = dt.code
                    WHERE dt.level < 10  -- 防止无限递归，根据实际层级调整
                )
                SELECT code, name, parent_id 
                FROM district_tree
                ORDER BY level, code
            """, [parent])
            
            rows = cursor.fetchall()
        
        if not rows:
            return self._build_response(
                data=[],
                message="未找到子节点",
                status=status.HTTP_200_OK,
            )
        
        # 构建节点字典和父子关系
        node_dict = {}
        
        # 先创建所有节点
        for code, name, parent_val in rows:
            node_dict[code] = {
                'parent': parent_val,
                'name': name,
                'code': code,
                'children': [],
            }
        
        # 建立父子关系，找出根节点
        root_nodes = []
        for code, name, parent_val in rows:
            if parent_val == parent:
                # 直接子节点就是根节点
                root_nodes.append(node_dict[code])
            elif parent_val in node_dict:
                # 建立父子关系
                node_dict[parent_val]['children'].append(node_dict[code])
        
        if (show_parent == True):
            parent_node = ExternalDistrictNode.objects.get(code=parent)
            root_nodes = {
                'parent': parent_node.parent_id,
                'name': parent_node.name,
                'code': parent_node.code,
                'children': root_nodes,
            }

        return self._build_response(
            data=root_nodes,
            message="ok",
            status=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=['get'])
    def tree_from_parent_2(self, request):
        """从选中的父级区县节点，构建树形结构"""
        parent = request.query_params.get('parent')

        from distutils.util import strtobool

        try:
            show_parent = bool(strtobool(request.query_params.get('show_parent', '0')))
        except ValueError:
            show_parent = False  # 无效值时的默认值
        
        if not parent:
            return self._build_response(
                data=[],
                message="parent参数不能为空",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # 使用批量查询减少数据库访问次数
        def get_all_descendants_batch(parents):
            """批量获取子孙节点，减少数据库查询次数"""
            if not parents:
                return []
            
            all_descendants = []
            current_level_codes = list(parents)
            
            while current_level_codes:
                # 批量查询当前层级的所有子节点
                children = ExternalDistrictNode.objects.filter(
                    parent_id__in=current_level_codes
                ).values('code', 'name', 'parent_id')
                
                if not children:
                    break
                    
                children_list = list(children)
                all_descendants.extend(children_list)
                
                # 准备下一层级的查询
                current_level_codes = [child['code'] for child in children_list]
            
            return all_descendants
        
        # 获取所有子孙节点
        all_nodes_data = get_all_descendants_batch([parent])
        
        if not all_nodes_data:
            return self._build_response(
                data=[],
                message="未找到子节点",
                status=status.HTTP_200_OK,
            )
        
        # 构建树结构
        node_dict = {}
        root_nodes = []
        
        # 创建所有节点
        for node_data in all_nodes_data:
            node_item = {
                'parent': node_data['parent_id'],
                'name': node_data['name'],
                'code': node_data['code'],
                'children': [],
            }
            node_dict[node_data['code']] = node_item
        
        # 建立父子关系
        for node_data in all_nodes_data:
            if node_data['parent_id'] == parent:
                root_nodes.append(node_dict[node_data['code']])
            elif node_data['parent_id'] in node_dict:
                node_dict[node_data['parent_id']]['children'].append(node_dict[node_data['code']])

        if (show_parent == True):
            parent_node = ExternalDistrictNode.objects.get(code=parent)
            root_nodes = {
                'parent': parent_node.parent_id,
                'name': parent_node.name,
                'code': parent_node.code,
                'children': root_nodes,
            }

        return self._build_response(
            data=root_nodes,
            message="ok",
            status=status.HTTP_200_OK,
        )


# 移入urls中
# router.register(r'external_district_node', views.ExternalDistrictNodeViewSet)
# 移入 __init__.py
# from external_platform.views.external_district_node import ExternalDistrictNodeViewSet