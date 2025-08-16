"""
工单同步服务
处理工单数据的拉取、更新和同步逻辑
"""
import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import WorkOrderSystem, WorkOrder, WorkOrderSyncLog
from .adapters import WorkOrderAdapterFactory

logger = logging.getLogger(__name__)


class WorkOrderSyncService:
    """工单同步服务"""
    
    def __init__(self, system_config: WorkOrderSystem):
        self.system_config = system_config
        self.adapter = WorkOrderAdapterFactory.create_adapter(
            system_config.name.lower(), 
            system_config
        )
    
    def pull_work_orders(self, since: Optional[datetime] = None, limit: int = 100) -> Dict[str, Any]:
        """
        拉取外部工单系统的工单
        
        Args:
            since: 开始时间，如果为None则拉取所有工单
            limit: 限制数量
            
        Returns:
            同步结果统计
        """
        start_time = time.time()
        sync_log = None
        
        try:
            # 创建同步日志
            sync_log = WorkOrderSyncLog.objects.create(
                external_system=self.system_config,
                sync_type='pull',
                status='pending',
                creator='system'
            )
            
            # 验证认证
            if not self.adapter.authenticate():
                raise Exception("认证失败")
            
            # 获取外部工单列表
            external_work_orders = self.adapter.get_work_orders(since=since, limit=limit)
            
            success_count = 0
            failed_count = 0
            error_messages = []
            
            # 批量处理工单
            with transaction.atomic():
                for external_work_order in external_work_orders:
                    try:
                        self._process_work_order(external_work_order)
                        success_count += 1
                    except Exception as e:
                        failed_count += 1
                        error_msg = f"处理工单 {external_work_order.get('external_id', 'unknown')} 失败: {str(e)}"
                        error_messages.append(error_msg)
                        logger.error(error_msg)
            
            # 更新同步日志
            execution_time = time.time() - start_time
            total_count = len(external_work_orders)
            
            if failed_count == 0:
                status = 'success'
            elif success_count > 0:
                status = 'partial'
            else:
                status = 'failed'
            
            sync_log.status = status
            sync_log.total_count = total_count
            sync_log.success_count = success_count
            sync_log.failed_count = failed_count
            sync_log.error_message = '\n'.join(error_messages) if error_messages else None
            sync_log.execution_time = execution_time
            sync_log.save()
            
            # 更新系统配置的最后同步时间
            self.system_config.last_sync_time = timezone.now()
            self.system_config.save(update_fields=['last_sync_time'])
            
            logger.info(f"工单拉取完成: 系统={self.system_config.name}, "
                       f"总数={total_count}, 成功={success_count}, 失败={failed_count}")
            
            return {
                'status': status,
                'total_count': total_count,
                'success_count': success_count,
                'failed_count': failed_count,
                'execution_time': execution_time,
                'error_messages': error_messages
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"工单拉取失败: {str(e)}"
            logger.error(error_msg)
            
            if sync_log:
                sync_log.status = 'failed'
                sync_log.error_message = error_msg
                sync_log.execution_time = execution_time
                sync_log.save()
            
            raise
    
    def update_work_order(self, external_id: str, data: Dict[str, Any]) -> bool:
        """
        更新工单
        
        Args:
            external_id: 外部系统工单ID
            data: 更新数据
            
        Returns:
            是否更新成功
        """
        try:
            # 验证认证
            if not self.adapter.authenticate():
                raise Exception("认证失败")
            
            # 更新外部系统工单
            success = self.adapter.update_work_order(external_id, data)
            
            if success:
                # 更新本地工单数据
                try:
                    work_order = WorkOrder.objects.get(
                        external_system=self.system_config,
                        external_id=external_id
                    )
                    
                    # 更新工单字段
                    for field, value in data.items():
                        if hasattr(work_order, field) and field not in ['id', 'external_id', 'external_system']:
                            setattr(work_order, field, value)
                    
                    work_order.sync_status = 'success'
                    work_order.sync_error = None
                    work_order.save()
                    
                    logger.info(f"工单更新成功: {external_id}")
                    
                except WorkOrder.DoesNotExist:
                    logger.warning(f"本地工单不存在: {external_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"工单更新失败 {external_id}: {str(e)}")
            return False
    
    def sync_work_orders(self) -> Dict[str, Any]:
        """
        同步工单（拉取新工单并更新现有工单）
        
        Returns:
            同步结果统计
        """
        start_time = time.time()
        sync_log = None
        
        try:
            # 创建同步日志
            sync_log = WorkOrderSyncLog.objects.create(
                external_system=self.system_config,
                sync_type='sync',
                status='pending',
                creator='system'
            )
            
            # 获取上次同步时间
            since = self.system_config.last_sync_time
            if not since:
                # 如果没有上次同步时间，则同步最近7天的数据
                since = timezone.now() - timedelta(days=7)
            
            # 拉取工单
            pull_result = self.pull_work_orders(since=since)
            
            # 更新同步日志
            execution_time = time.time() - start_time
            sync_log.status = pull_result['status']
            sync_log.total_count = pull_result['total_count']
            sync_log.success_count = pull_result['success_count']
            sync_log.failed_count = pull_result['failed_count']
            sync_log.error_message = '\n'.join(pull_result['error_messages']) if pull_result['error_messages'] else None
            sync_log.execution_time = execution_time
            sync_log.save()
            
            return pull_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"工单同步失败: {str(e)}"
            logger.error(error_msg)
            
            if sync_log:
                sync_log.status = 'failed'
                sync_log.error_message = error_msg
                sync_log.execution_time = execution_time
                sync_log.save()
            
            raise
    
    def _process_work_order(self, external_work_order: Dict[str, Any]) -> WorkOrder:
        """
        处理单个工单数据
        
        Args:
            external_work_order: 外部工单数据
            
        Returns:
            处理后的工单对象
        """
        external_id = external_work_order.get('external_id')
        if not external_id:
            raise ValidationError("外部工单ID不能为空")
        
        # 尝试获取现有工单
        work_order, created = WorkOrder.objects.get_or_create(
            external_system=self.system_config,
            external_id=external_id,
            defaults={
                'title': external_work_order.get('title', ''),
                'description': external_work_order.get('description', ''),
                'status': external_work_order.get('status', 'pending'),
                'priority': external_work_order.get('priority', 'medium'),
                'reporter': external_work_order.get('reporter', ''),
                'reporter_email': external_work_order.get('reporter_email', ''),
                'assignee': external_work_order.get('assignee', ''),
                'assignee_email': external_work_order.get('assignee_email', ''),
                'reported_at': self._parse_datetime(external_work_order.get('reported_at')),
                'due_date': self._parse_datetime(external_work_order.get('due_date')),
                'resolved_at': self._parse_datetime(external_work_order.get('resolved_at')),
                'category': external_work_order.get('category', ''),
                'tags': external_work_order.get('tags', []),
                'sync_status': 'success',
                'creator': 'system'
            }
        )
        
        if not created:
            # 更新现有工单
            work_order.title = external_work_order.get('title', work_order.title)
            work_order.description = external_work_order.get('description', work_order.description)
            work_order.status = external_work_order.get('status', work_order.status)
            work_order.priority = external_work_order.get('priority', work_order.priority)
            work_order.reporter = external_work_order.get('reporter', work_order.reporter)
            work_order.reporter_email = external_work_order.get('reporter_email', work_order.reporter_email)
            work_order.assignee = external_work_order.get('assignee', work_order.assignee)
            work_order.assignee_email = external_work_order.get('assignee_email', work_order.assignee_email)
            work_order.due_date = self._parse_datetime(external_work_order.get('due_date'))
            work_order.resolved_at = self._parse_datetime(external_work_order.get('resolved_at'))
            work_order.category = external_work_order.get('category', work_order.category)
            work_order.tags = external_work_order.get('tags', work_order.tags)
            work_order.sync_status = 'success'
            work_order.sync_error = None
            work_order.modifier = 'system'
            work_order.save()
        
        return work_order
    
    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """解析日期时间字符串"""
        if not datetime_str:
            return None
        
        try:
            # 尝试多种日期格式
            formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(datetime_str, fmt)
                except ValueError:
                    continue
            
            # 如果都失败，返回None
            logger.warning(f"无法解析日期时间: {datetime_str}")
            return None
            
        except Exception as e:
            logger.error(f"日期时间解析错误: {datetime_str}, {str(e)}")
            return None


class WorkOrderSyncManager:
    """工单同步管理器"""
    
    @classmethod
    def sync_all_systems(cls) -> Dict[str, Any]:
        """同步所有启用的工单系统"""
        results = {}
        
        active_systems = WorkOrderSystem.objects.filter(is_active=True)
        
        for system in active_systems:
            try:
                service = WorkOrderSyncService(system)
                result = service.sync_work_orders()
                results[system.name] = result
            except Exception as e:
                logger.error(f"同步系统 {system.name} 失败: {str(e)}")
                results[system.name] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        return results
    
    @classmethod
    def sync_system_by_id(cls, system_id: int) -> Dict[str, Any]:
        """根据ID同步指定系统"""
        try:
            system = WorkOrderSystem.objects.get(id=system_id, is_active=True)
            service = WorkOrderSyncService(system)
            return service.sync_work_orders()
        except WorkOrderSystem.DoesNotExist:
            raise ValueError(f"工单系统不存在或未启用: {system_id}")
    
    @classmethod
    def get_sync_status(cls) -> Dict[str, Any]:
        """获取所有系统的同步状态"""
        systems = WorkOrderSystem.objects.all()
        status = {}
        
        for system in systems:
            last_sync = WorkOrderSyncLog.objects.filter(
                external_system=system
            ).order_by('-create_time').first()
            
            status[system.name] = {
                'is_active': system.is_active,
                'sync_interval': system.sync_interval,
                'last_sync_time': system.last_sync_time,
                'last_sync_status': last_sync.status if last_sync else None,
                'last_sync_error': last_sync.error_message if last_sync else None,
            }
        
        return status
