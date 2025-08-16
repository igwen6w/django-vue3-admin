"""
工单同步日志视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Avg, Sum, Q

from utils.custom_model_viewSet import CustomModelViewSet
from utils.resp import SuccessResponse, ErrorResponse
from .serializers import WorkOrderSyncLogSerializer
from ..models import WorkOrderSyncLog


class WorkOrderSyncLogViewSet(CustomModelViewSet):
    """
    工单同步日志视图集
    """
    queryset = WorkOrderSyncLog.objects.all()
    serializer_class = WorkOrderSyncLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['external_system', 'sync_type', 'status']
    search_fields = ['external_system__name']
    ordering_fields = ['create_time', 'execution_time', 'total_count', 'success_count', 'failed_count']
    ordering = ['-create_time']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取同步日志统计信息"""
        try:
            from django.db.models import Count, Avg, Sum
            from django.utils import timezone
            from datetime import timedelta
            
            # 基础统计
            total_logs = WorkOrderSyncLog.objects.count()
            success_logs = WorkOrderSyncLog.objects.filter(status='success').count()
            failed_logs = WorkOrderSyncLog.objects.filter(status='failed').count()
            partial_logs = WorkOrderSyncLog.objects.filter(status='partial').count()
            
            # 按类型统计
            pull_logs = WorkOrderSyncLog.objects.filter(sync_type='pull').count()
            update_logs = WorkOrderSyncLog.objects.filter(sync_type='update').count()
            sync_logs = WorkOrderSyncLog.objects.filter(sync_type='sync').count()
            
            # 按系统统计
            system_stats = WorkOrderSyncLog.objects.values('external_system__name').annotate(
                total_count=Count('id'),
                success_count=Count('id', filter=Q(status='success')),
                failed_count=Count('id', filter=Q(status='failed')),
                avg_execution_time=Avg('execution_time')
            ).order_by('-total_count')
            
            # 最近7天的统计
            seven_days_ago = timezone.now() - timedelta(days=7)
            recent_logs = WorkOrderSyncLog.objects.filter(create_time__gte=seven_days_ago)
            recent_success = recent_logs.filter(status='success').count()
            recent_failed = recent_logs.filter(status='failed').count()
            
            # 平均执行时间
            avg_execution_time = WorkOrderSyncLog.objects.aggregate(
                avg_time=Avg('execution_time')
            )['avg_time'] or 0
            
            # 总处理工单数
            total_processed = WorkOrderSyncLog.objects.aggregate(
                total=Sum('total_count'),
                success=Sum('success_count'),
                failed=Sum('failed_count')
            )
            
            data = {
                'total_logs': total_logs,
                'success_logs': success_logs,
                'failed_logs': failed_logs,
                'partial_logs': partial_logs,
                'pull_logs': pull_logs,
                'update_logs': update_logs,
                'sync_logs': sync_logs,
                'system_stats': list(system_stats),
                'recent_7_days': {
                    'total': recent_logs.count(),
                    'success': recent_success,
                    'failed': recent_failed,
                },
                'avg_execution_time': round(avg_execution_time, 2),
                'total_processed': {
                    'total': total_processed['total'] or 0,
                    'success': total_processed['success'] or 0,
                    'failed': total_processed['failed'] or 0,
                }
            }
            
            return SuccessResponse(data=data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取统计信息失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_system(self, request):
        """按系统获取同步日志"""
        try:
            system_id = request.query_params.get('system_id')
            if not system_id:
                return ErrorResponse(message='请提供system_id参数')
            
            logs = WorkOrderSyncLog.objects.filter(external_system_id=system_id)
            
            page = self.paginate_queryset(logs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(logs, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取同步日志失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """按状态获取同步日志"""
        try:
            status = request.query_params.get('status')
            if not status:
                return ErrorResponse(message='请提供status参数')
            
            logs = WorkOrderSyncLog.objects.filter(status=status)
            
            page = self.paginate_queryset(logs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(logs, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取同步日志失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按类型获取同步日志"""
        try:
            sync_type = request.query_params.get('sync_type')
            if not sync_type:
                return ErrorResponse(message='请提供sync_type参数')
            
            logs = WorkOrderSyncLog.objects.filter(sync_type=sync_type)
            
            page = self.paginate_queryset(logs)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(logs, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取同步日志失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def recent_failures(self, request):
        """获取最近的失败日志"""
        try:
            limit = int(request.query_params.get('limit', 10))
            
            failed_logs = WorkOrderSyncLog.objects.filter(
                status='failed'
            ).order_by('-create_time')[:limit]
            
            serializer = self.get_serializer(failed_logs, many=True)
            return SuccessResponse(data=serializer.data)
            
        except Exception as e:
            return ErrorResponse(message=f'获取失败日志失败: {str(e)}')

    @action(detail=False, methods=['get'])
    def performance_analysis(self, request):
        """性能分析"""
        try:
            from django.db.models import Avg, Max, Min
            from django.utils import timezone
            from datetime import timedelta
            
            # 获取时间范围
            days = int(request.query_params.get('days', 7))
            start_date = timezone.now() - timedelta(days=days)
            
            # 按系统分析性能
            performance_stats = WorkOrderSyncLog.objects.filter(
                create_time__gte=start_date
            ).values('external_system__name').annotate(
                avg_execution_time=Avg('execution_time'),
                max_execution_time=Max('execution_time'),
                min_execution_time=Min('execution_time'),
                total_runs=Count('id'),
                success_rate=Count('id', filter=Q(status='success')) * 100.0 / Count('id')
            ).order_by('-avg_execution_time')
            
            # 按时间分析趋势
            daily_stats = WorkOrderSyncLog.objects.filter(
                create_time__gte=start_date
            ).extra(
                select={'date': 'DATE(create_time)'}
            ).values('date').annotate(
                total_runs=Count('id'),
                success_runs=Count('id', filter=Q(status='success')),
                avg_execution_time=Avg('execution_time')
            ).order_by('date')
            
            data = {
                'performance_by_system': list(performance_stats),
                'daily_trends': list(daily_stats),
                'analysis_period': f'最近{days}天'
            }
            
            return SuccessResponse(data=data)
            
        except Exception as e:
            return ErrorResponse(message=f'性能分析失败: {str(e)}')
