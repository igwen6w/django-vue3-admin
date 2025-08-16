"""
工单系统配置视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.custom_model_viewSet import CustomModelViewSet
from utils.resp import SuccessResponse, ErrorResponse
from .serializers import WorkOrderSystemSerializer
from ..models import WorkOrderSystem
from ..services import WorkOrderSyncManager
from ..tasks import sync_work_order, get_sync_status


class WorkOrderSystemViewSet(CustomModelViewSet):
    """
    工单系统配置视图集
    """
    queryset = WorkOrderSystem.objects.all()
    serializer_class = WorkOrderSystemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'name']
    search_fields = ['name', 'api_url']
    ordering_fields = ['create_time', 'update_time', 'name']
    ordering = ['-create_time']

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """同步指定工单系统"""
        try:
            system = self.get_object()
            
            # 异步执行同步任务
            task = sync_work_order.delay(system.id)
            
            return SuccessResponse(
                data={
                    'message': f'同步任务已提交，系统: {system.name}',
                    'task_id': task.id
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'同步失败: {str(e)}')

    @action(detail=False, methods=['post'])
    def sync_all(self, request):
        """同步所有启用的工单系统"""
        try:
            from ..tasks import sync_work_order_data
            task = sync_work_order_data.delay()
            
            return SuccessResponse(
                data={
                    'message': '所有系统同步任务已提交',
                    'task_id': task.id
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'同步失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def sync_status(self, request):
        """获取所有系统的同步状态"""
        try:
            task = get_sync_status.delay()
            
            return SuccessResponse(
                data={
                    'message': '同步状态查询任务已提交',
                    'task_id': task.id
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'获取状态失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def supported_systems(self, request):
        """获取支持的外部工单系统类型"""
        from ..adapters import WorkOrderAdapterFactory
        
        try:
            systems = WorkOrderAdapterFactory.get_supported_systems()
            
            return SuccessResponse(
                data={
                    'supported_systems': systems,
                    'message': '获取支持的系统类型成功'
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'获取支持的系统类型失败: {str(e)}')

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """测试工单系统连接"""
        try:
            system = self.get_object()
            
            # 创建适配器并测试连接
            from ..adapters import WorkOrderAdapterFactory
            adapter = WorkOrderAdapterFactory.create_adapter(system.name.lower(), system)
            
            if adapter.authenticate():
                return SuccessResponse(
                    data={
                        'message': f'连接测试成功，系统: {system.name}',
                        'system_name': system.name
                    }
                )
            else:
                return ErrorResponse(message=f'连接测试失败，系统: {system.name}')
                
        except Exception as e:
            return ErrorResponse(message=f'连接测试失败: {str(e)}')

    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        """启用工单系统"""
        try:
            system = self.get_object()
            system.is_active = True
            system.save()
            
            return SuccessResponse(
                data={
                    'message': f'工单系统已启用: {system.name}',
                    'system_name': system.name
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'启用失败: {str(e)}')

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """禁用工单系统"""
        try:
            system = self.get_object()
            system.is_active = False
            system.save()
            
            return SuccessResponse(
                data={
                    'message': f'工单系统已禁用: {system.name}',
                    'system_name': system.name
                }
            )
        except Exception as e:
            return ErrorResponse(message=f'禁用失败: {str(e)}')
