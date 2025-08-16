"""
工单数据视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from utils.custom_model_viewSet import CustomModelViewSet
from utils.resp import SuccessResponse, ErrorResponse
from .serializers import (
    WorkOrderSerializer, 
    WorkOrderUpdateSerializer,
    WorkOrderStatisticsSerializer
)
from ..models import WorkOrder
from ..tasks import update_work_order


class WorkOrderViewSet(CustomModelViewSet):
    """
    工单视图集
    """
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'external_system', 'sync_status']
    search_fields = ['title', 'description', 'reporter', 'assignee', 'external_id']
    ordering_fields = ['create_time', 'update_time', 'reported_at', 'due_date', 'priority']
    ordering = ['-create_time']

    def get_serializer_class(self):
        """根据操作类型选择序列化器"""
        if self.action in ['update', 'partial_update']:
            return WorkOrderUpdateSerializer
        return WorkOrderSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取工单统计信息"""
        try:
            # 基础统计
            total_count = WorkOrder.objects.count()
            pending_count = WorkOrder.objects.filter(status='pending').count()
            processing_count = WorkOrder.objects.filter(status='processing').count()
            resolved_count = WorkOrder.objects.filter(status='resolved').count()
            closed_count = WorkOrder.objects.filter(status='closed').count()
            cancelled_count = WorkOrder.objects.filter(status='cancelled').count()
            
            # 按优先级统计
            low_priority_count = WorkOrder.objects.filter(priority='low').count()
            medium_priority_count = WorkOrder.objects.filter(priority='medium').count()
            high_priority_count = WorkOrder.objects.filter(priority='high').count()
            urgent_priority_count = WorkOrder.objects.filter(priority='urgent').count()
            
            # 按系统统计
            system_stats = WorkOrder.objects.values('external_system__name').annotate(
                count=Count('id')
            ).order_by('-count')
            
            system_stats_dict = {item['external_system__name']: item['count'] for item in system_stats}
            
            # 最近7天的趋势
            seven_days_ago = timezone.now() - timedelta(days=7)
            recent_work_orders = WorkOrder.objects.filter(
                create_time__gte=seven_days_ago
            ).count()
            
            # 即将到期的工单
            upcoming_deadline = timezone.now() + timedelta(days=3)
            overdue_work_orders = WorkOrder.objects.filter(
                due_date__lt=timezone.now(),
                status__in=['pending', 'processing']
            ).count()
            
            upcoming_work_orders = WorkOrder.objects.filter(
                due_date__lte=upcoming_deadline,
                due_date__gt=timezone.now(),
                status__in=['pending', 'processing']
            ).count()
            
            data = {
                'total_count': total_count,
                'pending_count': pending_count,
                'processing_count': processing_count,
                'resolved_count': resolved_count,
                'closed_count': closed_count,
                'cancelled_count': cancelled_count,
                'low_priority_count': low_priority_count,
                'medium_priority_count': medium_priority_count,
                'high_priority_count': high_priority_count,
                'urgent_priority_count': urgent_priority_count,
                'system_stats': system_stats_dict,
                'recent_7_days_count': recent_work_orders,
                'overdue_count': overdue_work_orders,
                'upcoming_deadline_count': upcoming_work_orders,
            }
            
            serializer = WorkOrderStatisticsSerializer(data)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取统计信息失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """获取逾期工单"""
        try:
            overdue_work_orders = WorkOrder.objects.filter(
                due_date__lt=timezone.now(),
                status__in=['pending', 'processing']
            ).order_by('due_date')
            
            page = self.paginate_queryset(overdue_work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(overdue_work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取逾期工单失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def upcoming_deadline(self, request):
        """获取即将到期的工单"""
        try:
            days = int(request.query_params.get('days', 3))
            upcoming_deadline = timezone.now() + timedelta(days=days)
            
            upcoming_work_orders = WorkOrder.objects.filter(
                due_date__lte=upcoming_deadline,
                due_date__gt=timezone.now(),
                status__in=['pending', 'processing']
            ).order_by('due_date')
            
            page = self.paginate_queryset(upcoming_work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(upcoming_work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取即将到期工单失败: {str(e)}')

    @action(detail=True, methods=['post'])
    def update_external(self, request, pk=None):
        """更新外部系统工单"""
        try:
            work_order = self.get_object()
            
            # 获取更新数据
            update_data = request.data
            
            # 异步执行更新任务
            task = update_work_order.delay(
                system_id=work_order.external_system.id,
                external_id=work_order.external_id,
                data=update_data
            )
            
            return SuccessResponse(
                data={
                    'message': f'更新任务已提交，工单: {work_order.title}',
                    'task_id': task.id,
                    'external_id': work_order.external_id
                }
            )
            
        except Exception as e:
            return ErrorResponse(message=f'更新失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_system(self, request):
        """按系统获取工单"""
        try:
            system_id = request.query_params.get('system_id')
            if not system_id:
                return ErrorResponse(message='请提供system_id参数')
            
            work_orders = WorkOrder.objects.filter(external_system_id=system_id)
            
            page = self.paginate_queryset(work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取工单失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """按状态获取工单"""
        try:
            status = request.query_params.get('status')
            if not status:
                return ErrorResponse(message='请提供status参数')
            
            work_orders = WorkOrder.objects.filter(status=status)
            
            page = self.paginate_queryset(work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取工单失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """按优先级获取工单"""
        try:
            priority = request.query_params.get('priority')
            if not priority:
                return ErrorResponse(message='请提供priority参数')
            
            work_orders = WorkOrder.objects.filter(priority=priority)
            
            page = self.paginate_queryset(work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取工单失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索工单"""
        try:
            query = request.query_params.get('q', '')
            if not query:
                return ErrorResponse(message='请提供搜索关键词')
            
            work_orders = WorkOrder.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(reporter__icontains=query) |
                Q(assignee__icontains=query) |
                Q(external_id__icontains=query)
            )
            
            page = self.paginate_queryset(work_orders)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(work_orders, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'搜索失败: {str(e)}')
