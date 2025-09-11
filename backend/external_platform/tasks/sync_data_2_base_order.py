# -*- coding: utf-8 -*-

"""
同步数据到基础工单表任务
"""

import logging
import time
from typing import Dict, Any
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from external_platform.utils import get_task_config

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_data_2_base_order(self, work_order_meta_id: int) -> Dict[str, Any]:
    """将work_order_meta中的数据同步到work_order_base中
    
    从work_order_meta表的raw_data字段（JSON数组格式）中提取数据，
    根据字段映射关系转换后同步到work_order_base表中。
    
    raw_data格式示例:
    [
        {
            "fd_name": "roll_number",
            "type": "1", 
            "name": "工单编号",
            "choice_value": "250910171327424509",
            ...
        },
        ...
    ]
    
    Args:
        work_order_meta_id: work_order_meta记录的ID
        
    Returns:
        Dict[str, Any]: 任务执行结果，包含以下字段：
            - success: 是否成功
            - task_id: 任务ID
            - work_order_meta_id: 元数据记录ID
            - action: 执行动作（'created' 或 'updated'）
            - work_order_base_id: 基础记录ID
            - error: 错误信息（如果有）
    """
    task_id = self.request.id
    logger.info(f"开始同步工单数据到基础表 - 任务ID: {task_id}, Meta记录ID: {work_order_meta_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'task_id': task_id,
        'work_order_meta_id': work_order_meta_id,
        'action': None,  # 'created' 或 'updated'
        'work_order_base_id': None,
        'error': None
    }
    
    try:
        # 获取work_order_meta记录
        from work_order.models import Meta as WorkOrderMeta, Base as WorkOrderBase
        
        try:
            meta_record = WorkOrderMeta.objects.get(id=work_order_meta_id)
        except WorkOrderMeta.DoesNotExist:
            error_msg = f"WorkOrderMeta记录不存在: {work_order_meta_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 获取原始数据
        raw_data = meta_record.raw_data
        if not raw_data:
            error_msg = f"WorkOrderMeta记录缺少原始数据: {work_order_meta_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 构建字段映射 - external_前缀字段与raw_data中fd_name的映射
        field_mapping = {
            'external_roll_number': 'roll_number',
            'external_handle_rel_expire_time': 'handle_rel_expire_time',
            'external_src_way': 'src_way',
            'external_payroll_name': 'payroll_name',
            'external_company_tel': 'company_tel',
            'external_addr': 'addr',
            'external_region_district_id': 'region_district_id',
            'external_note14': 'note14',
            'external_distribute_way': 'distribute_way',
            'external_payroll_type': 'payroll_type',
            'external_event_type2_id': 'event_type2_id',
            'external_roll_content': 'roll_content',
            'external_note': 'note',
            'external_product_ids': 'product_ids',
            'external_addr2': 'addr2',
            'external_company_address': 'company_address',
            'external_order_number': 'order_number',
            'external_normal_payroll_title': 'normal_payroll_title',
            'external_addr3': 'addr3',
            'external_note1': 'note1',
            'external_note15': 'note15',
            'external_attachments': 'attachments',
            'external_note4': 'note4',
            'external_handling_quality': 'handling_quality',
            'external_note12': 'note12',
            'external_note2': 'note2',
            'external_note3': 'note3',
            'external_note16': 'note16',
            'external_note17': 'note17',
        }
        
        # 从raw_data中提取数据并转换
        sync_data = {}
        
        # 添加公共字段
        sync_data.update({
            'version': meta_record.version,
            'source_system': meta_record.source_system,
            'sync_task_id': task_id,
            'sync_status': True,
            'sync_time': timezone.now(),
        })
        
        # 添加external_id字段
        sync_data['external_id'] = int(meta_record.external_id)
        
        # 创建字段值映射字典，从raw_data数组中构建
        raw_data_dict = {}
        if isinstance(raw_data, list):
            logger.debug(f"处理raw_data数组，共{len(raw_data)}个字段配置")
            for item in raw_data:
                if isinstance(item, dict) and 'fd_name' in item:
                    fd_name = item.get('fd_name')
                    choice_value = item.get('choice_value')
                    # 过滤掉None值，但保留空字符串和0等有效值
                    if choice_value is not None:
                        raw_data_dict[fd_name] = choice_value
            logger.debug(f"成功提取{len(raw_data_dict)}个有效字段值")
        else:
            error_msg = f"WorkOrderMeta原始数据格式错误，期望数组格式: {work_order_meta_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 处理字段映射
        for external_field, fd_name in field_mapping.items():
            raw_value = raw_data_dict.get(fd_name)
            
            # 特殊处理某些字段
            if external_field == 'external_event_type2_id' and raw_value:
                # 处理数组字段，转换为字符串
                if isinstance(raw_value, list):
                    sync_data[external_field] = ', '.join(str(item) for item in raw_value)
                else:
                    sync_data[external_field] = str(raw_value) if raw_value else None
            elif external_field == 'external_attachments' and raw_value:
                # JSON字段保持原样
                sync_data[external_field] = raw_value
            elif raw_value is not None and raw_value != '':
                # 其他字段直接赋值，但确保不是None或空字符串
                sync_data[external_field] = str(raw_value)
            else:
                # 空值设置为None
                sync_data[external_field] = None
        
        # 检查是否已存在相同external_id的记录
        external_id = sync_data.get('external_id', 0)
        if not external_id:
            error_msg = f"缺少有效的external_id: {meta_record.external_id}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        with transaction.atomic():
            try:
                # 尝试获取现有记录
                existing_record = WorkOrderBase.objects.get(external_id=external_id)
                
                # 更新现有记录
                for field, value in sync_data.items():
                    setattr(existing_record, field, value)
                
                existing_record.save()
                
                result['action'] = 'updated'
                result['work_order_base_id'] = existing_record.id
                logger.info(f"更新工单基础记录 - external_id: {external_id}, 记录ID: {existing_record.id}")
                
            except WorkOrderBase.DoesNotExist:
                # 创建新记录
                new_record = WorkOrderBase.objects.create(**sync_data)
                
                result['action'] = 'created'
                result['work_order_base_id'] = new_record.id
                logger.info(f"创建工单基础记录 - external_id: {external_id}, 记录ID: {new_record.id}")
        
        # 更新meta记录的同步状态
        meta_record.sync_status = True
        meta_record.sync_time = timezone.now()
        meta_record.sync_task_id = task_id
        meta_record.save(update_fields=['sync_status', 'sync_time', 'sync_task_id', 'update_time'])
        
        result['success'] = True
        
        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"同步工单数据完成 - 任务ID: {task_id}, Meta记录ID: {work_order_meta_id}, "
                   f"动作: {result['action']}, 基础记录ID: {result['work_order_base_id']}, "
                   f"耗时: {execution_time}ms")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"同步工单数据异常: {str(e)}"
        logger.error(f"同步工单数据异常 - 任务ID: {task_id}, Meta记录ID: {work_order_meta_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('sync_data_2_base_order').get('retry_delay', 30)
            logger.info(f"同步工单数据重试 - 任务ID: {task_id}, Meta记录ID: {work_order_meta_id}, "
                       f"重试次数: {self.request.retries + 1}, 延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result