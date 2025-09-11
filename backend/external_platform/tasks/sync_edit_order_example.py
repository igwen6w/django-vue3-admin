# -*- coding: utf-8 -*-

"""
sync_edit_order 任务使用示例

演示如何使用编辑工单同步任务
"""

import logging
from external_platform.tasks.sync_edit_order import (
    sync_edit_order, 
    trigger_sync_edit_order,
    get_sync_task_status
)

logger = logging.getLogger(__name__)


def example_trigger_sync_manually():
    """手动触发编辑工单同步任务的示例"""
    
    # 假设有一个BaseEditRecord的ID
    edit_record_id = 123
    
    # 方式1：立即触发任务
    task_id = trigger_sync_edit_order(edit_record_id)
    if task_id:
        print(f"任务已触发，任务ID: {task_id}")
    else:
        print("任务触发失败")
    
    # 方式2：延迟30秒触发任务
    task_id = trigger_sync_edit_order(edit_record_id, delay=30)
    if task_id:
        print(f"延迟任务已触发，任务ID: {task_id}")
    
    # 方式3：直接调用Celery任务
    task_result = sync_edit_order.delay(edit_record_id)
    print(f"直接调用任务，任务ID: {task_result.id}")
    
    return task_result.id


def example_check_task_status():
    """检查任务状态的示例"""
    
    task_id = "your-task-id-here"
    
    # 获取任务状态
    status_info = get_sync_task_status(task_id)
    
    print(f"任务状态: {status_info}")
    
    # 根据状态进行不同处理
    if status_info['status'] == 'SUCCESS':
        print("任务执行成功")
        print(f"执行结果: {status_info['result']}")
    elif status_info['status'] == 'FAILURE':
        print("任务执行失败")
        print(f"错误信息: {status_info['error']}")
    elif status_info['status'] == 'PENDING':
        print("任务等待执行中")
    elif status_info['status'] == 'RETRY':
        print("任务重试中")
    else:
        print(f"任务状态: {status_info['status']}")


def example_batch_sync():
    """批量同步编辑记录的示例"""
    
    from work_order.models import BaseEditRecord
    
    # 获取未同步的编辑记录
    unsync_records = BaseEditRecord.objects.filter(sync_status=False)
    
    print(f"找到 {unsync_records.count()} 条未同步的编辑记录")
    
    task_ids = []
    
    for record in unsync_records:
        # 为每条记录触发同步任务，间隔10秒执行
        task_id = trigger_sync_edit_order(record.id, delay=len(task_ids) * 10)
        if task_id:
            task_ids.append(task_id)
            print(f"记录 {record.id} 同步任务已触发，任务ID: {task_id}")
        else:
            print(f"记录 {record.id} 同步任务触发失败")
    
    print(f"共触发 {len(task_ids)} 个同步任务")
    return task_ids


def example_sync_with_callback():
    """带回调处理的同步示例"""
    
    edit_record_id = 123
    
    # 触发任务
    task_id = trigger_sync_edit_order(edit_record_id)
    
    if not task_id:
        print("任务触发失败")
        return
    
    # 定期检查任务状态
    import time
    max_wait_time = 300  # 最多等待5分钟
    check_interval = 10   # 每10秒检查一次
    waited_time = 0
    
    while waited_time < max_wait_time:
        status_info = get_sync_task_status(task_id)
        
        if status_info['ready']:
            if status_info['successful']:
                print("同步成功！")
                print(f"结果: {status_info['result']}")
                
                # 这里可以添加成功后的处理逻辑
                handle_sync_success(edit_record_id, status_info['result'])
                break
                
            elif status_info['failed']:
                print("同步失败！")
                print(f"错误: {status_info['error']}")
                
                # 这里可以添加失败后的处理逻辑
                handle_sync_failure(edit_record_id, status_info['error'])
                break
        else:
            print(f"任务执行中... 状态: {status_info['status']}")
            time.sleep(check_interval)
            waited_time += check_interval
    
    if waited_time >= max_wait_time:
        print("任务执行超时")


def handle_sync_success(edit_record_id, result):
    """处理同步成功的回调"""
    print(f"编辑记录 {edit_record_id} 同步成功")
    
    # 这里可以添加成功后的业务逻辑
    # 比如发送通知、更新相关状态等
    pass


def handle_sync_failure(edit_record_id, error):
    """处理同步失败的回调"""
    print(f"编辑记录 {edit_record_id} 同步失败: {error}")
    
    # 这里可以添加失败后的业务逻辑
    # 比如记录错误日志、发送告警、重新排队等
    pass


if __name__ == "__main__":
    # 运行示例
    print("=== 手动触发同步任务示例 ===")
    example_trigger_sync_manually()
    
    print("\n=== 检查任务状态示例 ===")
    example_check_task_status()
    
    print("\n=== 批量同步示例 ===")
    example_batch_sync()
    
    print("\n=== 带回调处理的同步示例 ===")
    example_sync_with_callback()
