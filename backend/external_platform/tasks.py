# -*- coding: utf-8 -*-

"""
外部平台认证相关的Celery异步任务
"""

import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional
from celery import shared_task
from django.utils import timezone
from django.db import transaction


from external_platform.models import Platform, AuthSession, PlatformEndpoint
from external_platform.choices import PlatformAuthStatus
from external_platform.services.auth_service import AuthService
from external_platform.services.external_client import ExternalPlatformClient
from external_platform.services.request_log import (
    log_status_check_request, log_workorder_list_request,
    log_workorder_detail_request
)
from external_platform.utils import get_platform_config, get_task_config


logger = logging.getLogger(__name__)


def handle_session_expiry(response_data: Dict[str, Any], session: AuthSession, 
                         platform_sign: str, task_self=None, 
                         retry_delay: int = 60) -> bool:
    """
    检查并处理会话失效响应
    
    Args:
        response_data: API响应数据
        session: 当前认证会话
        platform_sign: 平台标识
        task_self: Celery任务实例（用于重试）
        retry_delay: 重试延迟秒数
        
    Returns:
        bool: True表示检测到会话失效，False表示会话正常
        
    Raises:
        Exception: 当需要重试任务时抛出异常
    """
    # 检查是否为会话失效响应
    if (response_data.get('status') == 'fail' and 
        response_data.get('des') == 'session失效' and 
        response_data.get('res') == ''):
        
        logger.warning(f"检测到会话失效 - 会话ID: {session.id}, "
                      f"平台: {platform_sign}")
        
        # 更新会话状态为过期
        with transaction.atomic():
            session.status = PlatformAuthStatus.EXPIRED
            session.save(update_fields=['status', 'update_time'])
        
        logger.info(f"已更新会话状态为过期 - 会话ID: {session.id}")
        
        # 触发重新登录任务
        login_task_id = AuthService.trigger_login_task(platform_sign)
        
        if login_task_id:
            logger.info(f"已触发重新登录任务 - 登录任务ID: {login_task_id}, "
                       f"平台: {platform_sign}")
            
            # 如果提供了任务实例且还有重试次数，则重试任务
            if task_self and task_self.request.retries < task_self.max_retries:
                task_id = task_self.request.id
                logger.info(f"会话失效，将在登录完成后重试 - 任务ID: {task_id}, "
                           f"重试次数: {task_self.request.retries + 1}, "
                           f"延迟: {retry_delay}秒")
                
                error_msg = f"会话失效已触发重新登录，任务将重试 - 登录任务ID: {login_task_id}"
                raise task_self.retry(countdown=retry_delay, exc=Exception(error_msg))
            
        else:
            logger.error(f"触发重新登录失败 - 平台: {platform_sign}")
        
        return True
    
    return False


@shared_task(bind=True, max_retries=3)
def login_task(self, platform_sign: str) -> Dict[str, Any]:
    """异步登录任务
    
    Args:
        platform_sign: 平台标识
        
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    logger.info(f"开始执行登录任务 - 任务ID: {task_id}, 平台: {platform_sign}")
    
    start_time = time.time()
    platform = None
    client = None
    
    try:
        # 获取平台配置
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"未找到平台配置: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 获取平台对象
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # 初始化客户端
        client = ExternalPlatformClient(platform_config['base_url'])
        
        # 执行登录流程
        result = client.execute_complete_login_flow(
            task_id, platform, platform_config
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        if result['success']:
            logger.info(f"登录任务完成 - 任务ID: {task_id}, 平台: {platform_sign}, "
                       f"耗时: {execution_time}ms")
        else:
            logger.error(f"登录任务失败 - 任务ID: {task_id}, 平台: {platform_sign}, "
                        f"耗时: {execution_time}ms, 错误: {result['error']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"登录任务异常: {str(e)}"
        logger.error(f"登录任务异常 - 任务ID: {task_id}, 平台: {platform_sign}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('login_task').get('retry_delay', 60)
            logger.info(f"登录任务重试 - 任务ID: {task_id}, 重试次数: {self.request.retries + 1}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return {'success': False, 'error': error_msg}
    
    finally:
        if client:
            client.close()


@shared_task
def maintain_auth_status_task() -> Dict[str, Any]:
    """维护认证状态的定时任务"""
    logger.info("开始执行认证状态维护任务")
    
    start_time = time.time()
    result = {
        'checked_count': 0,
        'refreshed_count': 0,
        'expired_count': 0,
        'error_count': 0
    }
    
    try:
        # 清理已过期的会话
        expired_count = AuthService.cleanup_expired_sessions()
        result['expired_count'] = expired_count
        
        # 获取即将过期的会话
        config = get_task_config('maintain_auth_status')
        refresh_before_hours = config.get('refresh_before_hours', 2)
        near_expiry_sessions = AuthService.get_sessions_near_expiry(refresh_before_hours)
        
        result['checked_count'] = len(near_expiry_sessions)
        
        # 触发刷新任务
        for session in near_expiry_sessions:
            try:
                # 请求 API 端点，检查登录状态
                # 使用 PlatformEndpoint endpoint_type 为 check_status 的端点来检查鉴权状态
                # response.res.card_number 为空时则表示会话过期
                
                # 获取状态检查端点
                try:
                    check_endpoint = PlatformEndpoint.objects.get(
                        platform=session.platform,
                        endpoint_type='check_status'
                    )
                except PlatformEndpoint.DoesNotExist:
                    logger.warning(f"平台 {session.platform.sign} 未配置状态检查端点")
                    continue
                
                # 获取平台配置
                platform_config = get_platform_config(session.platform.sign)
                if not platform_config:
                    logger.error(f"获取平台配置失败: {session.platform.sign}")
                    continue
                
                # 初始化客户端
                client = ExternalPlatformClient(platform_config['base_url'])
                
                try:
                    # 从会话中获取认证信息
                    auth_data = session.auth or {}
                    cookies = auth_data.get('cookies', {})
                    
                    # 发送状态检查请求
                    success, response_data, error_msg = client.make_authenticated_request(
                        method=check_endpoint.http_method,
                        endpoint=check_endpoint.path,
                        cookies=cookies
                    )
                    
                    # 记录请求日志
                    log_status_check_request(session, check_endpoint, success, response_data, error_msg)
                    
                    if success and response_data:
                        # 首先检查是否为会话失效响应
                        if handle_session_expiry(response_data, session, session.platform.sign):
                            # 会话失效已处理，无需进一步检查
                            pass
                        else:
                            # 检查响应中的 card_number 字段
                            res_data = response_data.get('res', {})
                            card_number = res_data.get('card_number', '')
                            
                            if not card_number:
                                # card_number 为空表示会话过期，更新会话状态
                                session.status = PlatformAuthStatus.EXPIRED
                                session.save(update_fields=['status', 'update_time'])
                                logger.info(f"会话已过期（card_number为空） - 会话ID: {session.id}, "
                                           f"平台: {session.platform.sign}, 账户: {session.account}")
                                
                                # 触发重新登录任务
                                login_task_id = AuthService.trigger_login_task(session.platform.sign)
                                if login_task_id:
                                    logger.info(f"已触发重新登录任务 - 登录任务ID: {login_task_id}, "
                                               f"平台: {session.platform.sign}")
                                else:
                                    logger.error(f"触发重新登录失败 - 平台: {session.platform.sign}")
                            else:
                                logger.info(f"会话状态正常 - 会话ID: {session.id}, "
                                           f"平台: {session.platform.sign}, 账户: {session.account}, "
                                           f"card_number: {card_number}")
                    else:
                        logger.warning(f"状态检查失败 - 会话ID: {session.id}, "
                                     f"错误: {error_msg}")
                
                finally:
                    client.close()

                logger.info(f"会话状态检查完成 - 会话ID: {session.id}, "
                           f"平台: {session.platform.sign}, 账户: {session.account}, "
                           f"过期时间: {session.expire_time}")
                result['refreshed_count'] += 1
                
            except Exception as e:
                logger.error(f"处理即将过期会话失败 - 会话ID: {session.id}, "
                            f"错误: {str(e)}", exc_info=True)
                result['error_count'] += 1
        
        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"认证状态维护任务完成 - 耗时: {execution_time}ms, "
                   f"检查: {result['checked_count']}, 刷新: {result['refreshed_count']}, "
                   f"过期: {result['expired_count']}, 错误: {result['error_count']}")
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"认证状态维护任务异常: {str(e)}"
        logger.error(f"认证状态维护任务异常 - 耗时: {execution_time}ms, 错误: {error_msg}", 
                    exc_info=True)
        result['error_count'] += 1
        return result


@shared_task(bind=True, max_retries=3)
def batch_fetch_workorders_task(self) -> Dict[str, Any]:
    """定时任务:批量获取市中心系统工单
    
    任务执行流程：
    0. 从 PlatformEndpoint endpoint_type = workorder_list 获取API端点和请求参数
    1. 构建请求参数
    2. 获取已鉴权会话句柄
    3. 请求端点获取工单列表
    4. 处理列表中的每个记录，创建获取单个工单详情任务
    5. 结束任务
    
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    platform_sign = 'city_center_workorder'
    
    logger.info(f"开始执行批量获取工单任务 - 任务ID: {task_id}, 平台: {platform_sign}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'task_id': task_id,
        'fetched_count': 0,
        'created_tasks': 0,
        'saved_records': 0,
        'updated_records': 0,
        'skipped_records': 0,
        'error': None
    }
    
    try:
        # 步骤0: 获取平台和工单列表端点配置
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        try:
            workorder_endpoint = PlatformEndpoint.objects.get(
                platform=platform,
                endpoint_type='workorder_list'
            )
        except PlatformEndpoint.DoesNotExist:
            error_msg = f"平台 {platform_sign} 未配置工单列表端点"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 步骤1: 构建请求参数
        base_payload = workorder_endpoint.payload or {}
        
        # 获取当前时间范围（默认获取最近30天的工单）
        from datetime import timedelta
        
        end_time = timezone.now()
        start_time_param = end_time - timedelta(days=30)
        
        request_payload = {
            **base_payload,
            'search_start_time': start_time_param.strftime('%Y-%m-%d %H:%M:%S'),
            'search_end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'page': 1,
            'pagesize': 50  # 每页获取50条记录
        }
        
        logger.info(f"构建请求参数完成 - 时间范围: {request_payload['search_start_time']} 到 {request_payload['search_end_time']}")
        
        # 步骤2: 获取已鉴权会话句柄
        try:
            active_session = AuthSession.objects.filter(
                platform=platform,
                status=PlatformAuthStatus.ACTIVE,
                expire_time__gt=timezone.now()
            ).first()
            
            if not active_session:
                # 发起登录
                AuthService.trigger_login_task(platform_sign)
                # 记录日志
                error_msg = "未找到有效的认证会话，请先执行登录任务"
                logger.warning(error_msg)
                result['error'] = error_msg
                return result
                
        except Exception as e:
            error_msg = f"获取认证会话失败: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 步骤3: 请求端点获取工单列表
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"获取平台配置失败: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        client = ExternalPlatformClient(platform_config['base_url'])
        
        try:
            # 从会话中获取认证信息
            auth_data = active_session.auth or {}
            cookies = auth_data.get('cookies', {})
            
            # 发送工单列表请求
            success, response_data, error_msg = client.make_authenticated_request(
                method=workorder_endpoint.http_method,
                endpoint=workorder_endpoint.path,
                cookies=cookies,
                data=request_payload if workorder_endpoint.http_method == 'POST' else None,
                params=request_payload if workorder_endpoint.http_method == 'GET' else None
            )
            
            # 记录请求日志
            log_workorder_list_request(active_session, workorder_endpoint, success, response_data, error_msg, request_payload)
            
            # 检查会话失效响应
            if success and response_data:
                try:
                    retry_delay = get_task_config('batch_fetch_workorders_task').get('retry_delay', 300)
                    if handle_session_expiry(response_data, active_session, platform_sign, 
                                           task_self=self, retry_delay=retry_delay):
                        # 如果检测到会话失效但无法重试，返回错误
                        error_msg = "会话失效且已达到最大重试次数或触发重新登录失败"
                        result['error'] = error_msg
                        return result
                except Exception as e:
                    # 如果是重试异常，重新抛出
                    if "会话失效已触发重新登录" in str(e):
                        raise
                    else:
                        error_msg = f"处理会话失效异常: {str(e)}"
                        logger.error(error_msg)
                        result['error'] = error_msg
                        return result
            
            if not success:
                error_msg = f"获取工单列表失败: {error_msg}"
                logger.error(error_msg)
                result['error'] = error_msg
                return result
            
            # 步骤4: 处理工单列表数据并存储到数据库
            workorder_list = []
            if response_data and 'res' in response_data:
                res_data = response_data['res']
                # 根据实际数据结构，工单列表在 tbody 字段中
                if isinstance(res_data, dict) and 'tbody' in res_data:
                    workorder_list = res_data['tbody']
                elif isinstance(res_data, dict) and 'list' in res_data:
                    workorder_list = res_data['list']
                elif isinstance(res_data, list):
                    workorder_list = res_data
            
            result['fetched_count'] = len(workorder_list)
            logger.info(f"获取到工单列表 - 数量: {result['fetched_count']}")
            
            # 步骤5: 存储工单数据到数据库并创建详情获取任务
            from work_order.models import Meta as WorkOrderMeta
            
            created_tasks = 0
            saved_records = 0
            skipped_records = 0
            
            for workorder in workorder_list:
                try:
                    # 根据实际数据结构，工单ID在 id 字段中
                    workorder_id = workorder.get('id')
                    if not workorder_id:
                        logger.warning(f"工单缺少ID字段 - 工单数据: {workorder}")
                        continue
                    
                    # 计算工单数据的MD5版本号
                    workorder_json = json.dumps(workorder, sort_keys=True, ensure_ascii=False)
                    current_version = hashlib.md5(workorder_json.encode('utf-8')).hexdigest()
                    
                    # 检查是否已存在相同工单ID的最新记录
                    existing_record = WorkOrderMeta.objects.filter(
                        external_id=int(workorder_id),
                        source_system=platform_sign
                    ).order_by('-create_time').first()
                    
                    should_save = False
                    
                    if not existing_record:
                        # 没有现有记录，直接创建新记录
                        should_save = True
                        logger.debug(f"工单ID {workorder_id} 无现有记录，将创建新记录")
                    elif existing_record.version != current_version:
                        # 版本不同，直接创建新记录
                        should_save = True
                        logger.info(f"工单ID {workorder_id} 版本不同，将创建新记录 - 旧版本: {existing_record.version[:8]}..., 新版本: {current_version[:8]}...")
                    else:
                        # 版本相同，跳过
                        skipped_records += 1
                        logger.debug(f"工单ID {workorder_id} 版本相同，跳过处理")
                        continue
                    
                    # 执行数据库操作
                    if should_save:
                        with transaction.atomic():
                            # 创建新记录
                            meta_record = WorkOrderMeta.objects.create(
                                version=current_version,
                                source_system=platform_sign,
                                sync_task_id=0,  # 将由fetch_single_workorder_task更新
                                raw_data=workorder,
                                pull_task_id=task_id,
                                external_id=int(workorder_id)
                            )
                            
                            saved_records += 1
                            logger.info(f"保存新工单记录 - 工单ID: {workorder_id}, 记录ID: {meta_record.id}")
                    
                    # 创建获取单个工单详情的任务
                    fetch_single_workorder_task.delay(
                        platform_sign=platform_sign,
                        workorder_id=workorder_id,
                        batch_task_id=task_id
                    )
                    created_tasks += 1
                    logger.debug(f"创建工单详情任务 - 工单ID: {workorder_id}, 工单类型: {workorder.get('payroll_type', '')}")
                    
                except Exception as e:
                    logger.error(f"处理工单数据失败 - 工单ID: {workorder.get('id', 'unknown')}, 错误: {str(e)}", exc_info=True)
            
            result['created_tasks'] = created_tasks
            result['saved_records'] = saved_records
            result['skipped_records'] = skipped_records
            result['success'] = True
            
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"批量获取工单任务完成 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                       f"获取数量: {result['fetched_count']}, 保存: {result['saved_records']}, "
                       f"跳过: {result['skipped_records']}, 创建任务: {result['created_tasks']}")
            
        finally:
            client.close()
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"批量获取工单任务异常: {str(e)}"
        logger.error(f"批量获取工单任务异常 - 任务ID: {task_id}, 耗时: {execution_time}ms, "
                    f"错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('batch_fetch_workorders_task').get('retry_delay', 300)  # 5分钟后重试
            logger.info(f"批量获取工单任务重试 - 任务ID: {task_id}, 重试次数: {self.request.retries + 1}, "
                       f"延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result


@shared_task(bind=True, max_retries=3)
def fetch_single_workorder_task(self, platform_sign: str, workorder_id: str, batch_task_id: str = None) -> Dict[str, Any]:
    """获取单个工单详情任务
    
    Args:
        platform_sign: 平台标识
        workorder_id: 工单ID
        batch_task_id: 批量任务ID（可选）
        
    Returns:
        任务执行结果
    """
    task_id = self.request.id
    logger.info(f"开始获取单个工单详情 - 任务ID: {task_id}, 平台: {platform_sign}, 工单ID: {workorder_id}")
    
    start_time = time.time()
    result = {
        'success': False,
        'platform_sign': platform_sign,
        'workorder_id': workorder_id,
        'task_id': task_id,
        'batch_task_id': batch_task_id,
        'error': None
    }
    
    try:
        # 获取平台配置
        try:
            platform = Platform.objects.get(sign=platform_sign, is_deleted=False)
        except Platform.DoesNotExist:
            error_msg = f"平台不存在: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 获取工单详情端点（假设端点类型为 workorder_detail）
        try:
            detail_endpoint = PlatformEndpoint.objects.get(
                platform=platform,
                endpoint_type='workorder_detail'
            )
        except PlatformEndpoint.DoesNotExist:
            error_msg = f"平台 {platform_sign} 未配置工单详情端点"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 获取认证会话
        try:
            active_session = AuthSession.objects.filter(
                platform=platform,
                status=PlatformAuthStatus.ACTIVE,
                expire_time__gt=timezone.now()
            ).first()
            
            if not active_session:
                error_msg = "未找到有效的认证会话"
                logger.warning(error_msg)
                result['error'] = error_msg
                return result
                
        except Exception as e:
            error_msg = f"获取认证会话失败: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        # 构建请求参数
        base_payload = detail_endpoint.payload or {}
        request_payload = {
            **base_payload,
            'payroll_id': workorder_id
        }
        
        # 获取平台配置并发送请求
        platform_config = get_platform_config(platform_sign)
        if not platform_config:
            error_msg = f"获取平台配置失败: {platform_sign}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
        
        client = ExternalPlatformClient(platform_config['base_url'])
        
        try:
            # 从会话中获取认证信息
            auth_data = active_session.auth or {}
            cookies = auth_data.get('cookies', {})
            
            # 发送工单详情请求
            success, response_data, error_msg = client.make_authenticated_request(
                method=detail_endpoint.http_method,
                endpoint=detail_endpoint.path,
                cookies=cookies,
                data=request_payload if detail_endpoint.http_method == 'POST' else None,
                params=request_payload if detail_endpoint.http_method == 'GET' else None
            )
            
            # 记录请求日志
            log_workorder_detail_request(active_session, detail_endpoint, success, response_data, error_msg, request_payload)
            
            # 检查会话失效响应
            if success and response_data:
                try:
                    retry_delay = get_task_config('fetch_single_workorder_task').get('retry_delay', 60)
                    if handle_session_expiry(response_data, active_session, platform_sign, 
                                           task_self=self, retry_delay=retry_delay):
                        # 如果检测到会话失效但无法重试，返回错误
                        error_msg = "会话失效且已达到最大重试次数或触发重新登录失败"
                        result['error'] = error_msg
                        return result
                except Exception as e:
                    # 如果是重试异常，重新抛出
                    if "会话失效已触发重新登录" in str(e):
                        raise
                    else:
                        error_msg = f"处理会话失效异常: {str(e)}"
                        logger.error(error_msg)
                        result['error'] = error_msg
                        return result
            
            if not success:
                error_msg = f"获取工单详情失败: {error_msg}"
                logger.error(error_msg)
                result['error'] = error_msg
                return result
            
            # 保存原始工单数据
            if response_data:
                from work_order.models import Meta as WorkOrderMeta
                
                # 创建原始工单记录
                meta_record = WorkOrderMeta.objects.create(
                    version='1.0',
                    source_system=platform_sign,
                    sync_task_id=int(task_id.replace('-', '')[:10], 16),  # 将任务ID转换为数字
                    raw_data=response_data,
                    pull_task_id=int(batch_task_id.replace('-', '')[:10], 16) if batch_task_id else 0
                )
                
                logger.info(f"保存原始工单成功 - 工单ID: {workorder_id}, 记录ID: {meta_record.id}")
                result['meta_record_id'] = meta_record.id
            
            result['success'] = True
            
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"获取单个工单详情完成 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                       f"耗时: {execution_time}ms")
            
        finally:
            client.close()
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        error_msg = f"获取单个工单详情异常: {str(e)}"
        logger.error(f"获取单个工单详情异常 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                    f"耗时: {execution_time}ms, 错误: {error_msg}", exc_info=True)
        
        result['error'] = error_msg
        
        # 重试逻辑
        if self.request.retries < self.max_retries:
            retry_delay = get_task_config('fetch_single_workorder_task').get('retry_delay', 60)
            logger.info(f"获取单个工单详情重试 - 任务ID: {task_id}, 工单ID: {workorder_id}, "
                       f"重试次数: {self.request.retries + 1}, 延迟: {retry_delay}秒")
            raise self.retry(countdown=retry_delay, exc=e)
        
        return result
