# -*- coding: utf-8 -*-

"""
工单相关信号处理器
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from work_order.models import BaseEditRecord

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseEditRecord)
def handle_base_edit_record_created(sender, instance, created, **kwargs):
    """处理BaseEditRecord创建后的信号
    
    当用户添加编辑记录后，自动触发同步任务
    """
    if created:
        logger.info(f"检测到新的编辑记录创建 - ID: {instance.id}, external_id: {instance.external_id}")
        
        # 导入任务函数
        from external_platform.tasks.sync_edit_order import trigger_sync_edit_order
        
        # 触发同步任务，延迟5秒执行以确保数据库事务完成
        task_id = trigger_sync_edit_order(instance.id, delay=5)
        
        if task_id:
            logger.info(f"编辑工单同步任务已触发 - 编辑记录ID: {instance.id}, 任务ID: {task_id}")
        else:
            logger.error(f"编辑工单同步任务触发失败 - 编辑记录ID: {instance.id}")
