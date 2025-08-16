"""
工单同步 Celery 任务
"""
import logging
from celery import shared_task
from django.utils import timezone

from .services import WorkOrderSyncManager, WorkOrderSyncService
from .models import WorkOrderSystem

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='work_order.pull_work_orders')
def pull_work_order(self, system_id: int = None, since: str = None, limit: int = 100):
    """
    拉取工单任务
    
    Args:
        system_id: 工单系统ID，如果为None则拉取所有系统
        since: 开始时间字符串，格式：YYYY-MM-DD HH:MM:SS
        limit: 限制数量
    """
    try:
        if system_id:
            # 拉取指定系统
            result = WorkOrderSyncManager.sync_system_by_id(system_id)
            logger.info(f"拉取工单完成 - 系统ID: {system_id}, 结果: {result}")
            return result
        else:
            # 拉取所有系统
            results = WorkOrderSyncManager.sync_all_systems()
            logger.info(f"拉取工单完成 - 所有系统, 结果: {results}")
            return results
            
    except Exception as e:
        logger.error(f"拉取工单失败: {str(e)}")
        # 重新抛出异常，让Celery知道任务失败
        raise


@shared_task(bind=True, name='work_order.update_work_order')
def update_work_order(self, system_id: int, external_id: str, data: dict):
    """
    更新工单任务
    
    Args:
        system_id: 工单系统ID
        external_id: 外部系统工单ID
        data: 更新数据
    """
    try:
        system = WorkOrderSystem.objects.get(id=system_id, is_active=True)
        service = WorkOrderSyncService(system)
        success = service.update_work_order(external_id, data)
        
        if success:
            logger.info(f"更新工单成功 - 系统: {system.name}, 工单ID: {external_id}")
        else:
            logger.error(f"更新工单失败 - 系统: {system.name}, 工单ID: {external_id}")
        
        return {'success': success, 'system': system.name, 'external_id': external_id}
        
    except WorkOrderSystem.DoesNotExist:
        error_msg = f"工单系统不存在或未启用: {system_id}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        logger.error(f"更新工单失败: {str(e)}")
        raise


@shared_task(bind=True, name='work_order.sync_work_orders')
def sync_work_order(self, system_id: int = None):
    """
    同步工单任务（拉取新工单并更新现有工单）
    
    Args:
        system_id: 工单系统ID，如果为None则同步所有系统
    """
    try:
        if system_id:
            # 同步指定系统
            result = WorkOrderSyncManager.sync_system_by_id(system_id)
            logger.info(f"同步工单完成 - 系统ID: {system_id}, 结果: {result}")
            return result
        else:
            # 同步所有系统
            results = WorkOrderSyncManager.sync_all_systems()
            logger.info(f"同步工单完成 - 所有系统, 结果: {results}")
            return results
            
    except Exception as e:
        logger.error(f"同步工单失败: {str(e)}")
        raise


@shared_task(bind=True, name='work_order.sync_work_order_data')
def sync_work_order_data(self):
    """
    同步工单数据任务（定时任务）
    这个任务会被Celery Beat定时调用
    """
    try:
        # 获取所有启用的工单系统
        active_systems = WorkOrderSystem.objects.filter(is_active=True)
        
        if not active_systems.exists():
            logger.info("没有启用的工单系统，跳过同步")
            return {'message': '没有启用的工单系统'}
        
        # 同步所有系统
        results = WorkOrderSyncManager.sync_all_systems()
        
        # 统计结果
        total_systems = len(active_systems)
        success_systems = sum(1 for result in results.values() if result.get('status') == 'success')
        failed_systems = total_systems - success_systems
        
        logger.info(f"定时同步工单完成 - 总系统: {total_systems}, 成功: {success_systems}, 失败: {failed_systems}")
        
        return {
            'total_systems': total_systems,
            'success_systems': success_systems,
            'failed_systems': failed_systems,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"定时同步工单失败: {str(e)}")
        raise


@shared_task(bind=True, name='work_order.get_sync_status')
def get_sync_status(self):
    """
    获取同步状态任务
    """
    try:
        status = WorkOrderSyncManager.get_sync_status()
        logger.info(f"获取同步状态完成: {status}")
        return status
    except Exception as e:
        logger.error(f"获取同步状态失败: {str(e)}")
        raise


@shared_task(bind=True, name='work_order.clean_old_sync_logs')
def clean_old_sync_logs(self, days: int = 30):
    """
    清理旧的同步日志任务
    
    Args:
        days: 保留天数，默认30天
    """
    try:
        from .models import WorkOrderSyncLog
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = WorkOrderSyncLog.objects.filter(
            create_time__lt=cutoff_date
        ).delete()
        
        logger.info(f"清理同步日志完成 - 删除 {deleted_count} 条记录")
        return {'deleted_count': deleted_count}
        
    except Exception as e:
        logger.error(f"清理同步日志失败: {str(e)}")
        raise