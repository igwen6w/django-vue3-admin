# -*- coding: utf-8 -*-

"""
外部平台认证相关的Celery异步任务
"""

# 导入所有任务，确保Celery能够发现它们
from external_platform.tasks.batch_fetch_workorders_task import batch_fetch_workorders_task
from external_platform.tasks.fetch_single_workorder_task import fetch_single_workorder_task
from external_platform.tasks.sync_data_2_base_order import sync_data_2_base_order
from external_platform.tasks.sync_edit_order import sync_edit_order

__all__ = [
    'batch_fetch_workorders_task',
    'fetch_single_workorder_task',
    'sync_data_2_base_order',
    'sync_edit_order',
]