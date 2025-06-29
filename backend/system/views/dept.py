from datetime import timezone, datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from system.models import Dept
from utils.custom_model_viewSet import CustomModelViewSet


class DeptSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    children = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ['id', 'create_time']

    def get_children(self, obj):
        """获取子部门"""
        children = obj.children.all().order_by('id')
        if children:
            return DeptSerializer(children, many=True).data
        return []

    def get_status_text(self, obj):
        """获取状态文本"""
        return obj.get_status_display()


class DeptViewSet(CustomModelViewSet):
    """部门管理视图集"""
    queryset = Dept.objects.filter(pid__isnull=True).order_by('id', 'status')
    serializer_class = DeptSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'pid']
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']

    def perform_create(self, serializer):
        # 自动设置创建时间
        if 'create_time' not in serializer.validated_data:
            serializer.validated_data['create_time'] = datetime.now()
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs['pk']
        instance = Dept.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        headers = self.get_success_headers(serializer.data)
        return self._build_response(
            data=serializer.data,
            message="ok",
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instance = Dept.objects.get(pk=pk)
        self.perform_destroy(instance)
        return self._build_response(
            message="ok",
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取部门树形结构"""
        queryset = self.get_queryset().filter(pid__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

