from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as filters

from system.models import RolePermission, Menu, Role
from utils.custom_model_viewSet import CustomModelViewSet
from utils.serializers import CustomModelSerializer


class RoleSerializer(CustomModelSerializer):
    """角色序列化器"""
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        many=True,
        required=False
    )
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['id', 'create_time']

    def get_status_text(self, obj):
        """获取状态文本"""
        return obj.get_status_display()


class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status')  # 保持精确，如需模糊可改为 icontains

    class Meta:
        model = Role
        fields = ['status', 'name', 'code']


class RoleViewSet(CustomModelViewSet):
    """角色管理视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoleFilter
    search_fields = ['name']
    ordering_fields = ['create_time']

    @action(detail=True, methods=['post'])
    def assign_permissions(self, request, pk=None):
        """分配角色权限"""
        role = self.get_object()
        menu_ids = request.data.get('menu_ids', [])

        # 清除原有权限
        role.permissions.clear()

        # 添加新权限
        for menu_id in menu_ids:
            menu = get_object_or_404(Menu, id=menu_id)
            RolePermission.objects.create(role=role, menu=menu)

        serializer = self.get_serializer(role)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # 获取请求数据
        data = request.data.copy()
        permissions = data.pop('permissions', [])  # 提取权限列表

        # 创建角色（不包含权限）
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        # 处理权限关联（可根据需求自定义）
        if permissions:
            try:
                # 验证权限ID是否存在
                valid_permissions = Menu.objects.filter(id__in=permissions)

                # 创建中间表记录（如果需要保存额外字段）
                for menu in valid_permissions:
                    RolePermission.objects.create(
                        role=role,
                        menu=menu,
                    )
            except Exception as e:
                # 如果关联失败，删除已创建的角色
                role.delete()
                return Response(
                    {'error': f'权限关联失败: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return self._build_response(
            data=serializer.data,
            message="ok",
            status=status.HTTP_200_OK,
        )
