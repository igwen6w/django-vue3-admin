# -*- coding: utf-8 -*-

"""
认证相关API视图
"""

import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from celery.result import AsyncResult

from external_platform.services.auth_service import AuthService
from external_platform.models import Platform
from external_platform.serializers import (
    AuthStatusResponseSerializer, LoginRequestSerializer, LoginResponseSerializer,
    TaskStatusResponseSerializer, SessionListResponseSerializer, 
    RefreshSessionRequestSerializer, SessionInfoSerializer
)
from external_platform.utils import format_session_info

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_auth_status(request, platform_sign, account):
    """获取认证状态
    
    Args:
        platform_sign: 平台标识
        account: 账户名
        
    Returns:
        认证状态信息
    """
    logger.info(f"查询认证状态 - 平台: {platform_sign}, 账户: {account}, "
               f"请求用户: {request.user.username}")
    
    try:
        # 获取有效会话
        session = AuthService.get_valid_session(platform_sign, account)
        
        if session:
            session_info = AuthService.get_session_info(session)
            formatted_session = format_session_info(session_info)
            logger.info(f"认证状态查询成功 - 平台: {platform_sign}, 账户: {account}, "
                       f"会话ID: {session.id}")
            
            response_data = {
                'success': True,
                'authenticated': True,
                'session': formatted_session
            }
            serializer = AuthStatusResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.info(f"未找到有效认证会话 - 平台: {platform_sign}, 账户: {account}")
            
            response_data = {
                'success': True,
                'authenticated': False,
                'message': '未找到有效认证会话'
            }
            serializer = AuthStatusResponseSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    except Exception as e:
        error_msg = f"查询认证状态异常: {str(e)}"
        logger.error(f"认证状态查询异常 - 平台: {platform_sign}, 账户: {account}, "
                    f"错误: {error_msg}", exc_info=True)
        
        return Response({
            'success': False,
            'error': error_msg
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_login(request):
    """触发登录任务
    
    Request Body:
        {
            "platform_sign": "city_center_workorder",
            "account": "username",
            "password": "password"
        }
        
    Returns:
        任务信息
    """
    logger.info(f"触发登录任务请求 - 请求用户: {request.user.username}")
    
    try:
        # 验证请求数据
        serializer = LoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"登录任务参数验证失败 - 错误: {serializer.errors}")
            
            response_data = {
                'success': False,
                'error': '请求参数验证失败',
                'details': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        platform_sign = validated_data['platform_sign']
        account = validated_data['account']
        password = validated_data['password']
        
        # 触发登录任务
        task_id = AuthService.trigger_login_task(platform_sign, account, password)
        
        if task_id:
            logger.info(f"登录任务触发成功 - 任务ID: {task_id}, 平台: {platform_sign}, "
                       f"账户: {account}")
            
            return Response({
                'success': True,
                'task_id': task_id,
                'message': '登录任务已触发'
            }, status=status.HTTP_202_ACCEPTED)
        else:
            error_msg = "触发登录任务失败"
            logger.error(f"登录任务触发失败 - 平台: {platform_sign}, 账户: {account}")
            
            return Response({
                'success': False,
                'error': error_msg
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        error_msg = f"触发登录任务异常: {str(e)}"
        logger.error(f"登录任务触发异常 - 错误: {error_msg}", exc_info=True)
        
        return Response({
            'success': False,
            'error': error_msg
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status(request, task_id):
    """查询任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务状态信息
    """
    logger.info(f"查询任务状态 - 任务ID: {task_id}, 请求用户: {request.user.username}")
    
    try:
        # 获取任务结果
        result = AsyncResult(task_id)
        
        task_info = {
            'task_id': task_id,
            'status': result.status,
            'ready': result.ready(),
            'successful': result.successful() if result.ready() else None,
            'failed': result.failed() if result.ready() else None
        }
        
        # 如果任务完成，获取结果
        if result.ready():
            if result.successful():
                task_info['result'] = result.result
                logger.info(f"任务查询成功 - 任务ID: {task_id}, 状态: {result.status}")
            else:
                task_info['error'] = str(result.result) if result.result else "任务执行失败"
                logger.warning(f"任务执行失败 - 任务ID: {task_id}, 错误: {task_info['error']}")
        else:
            logger.info(f"任务进行中 - 任务ID: {task_id}, 状态: {result.status}")
        
        return Response({
            'success': True,
            'task': task_info
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        error_msg = f"查询任务状态异常: {str(e)}"
        logger.error(f"任务状态查询异常 - 任务ID: {task_id}, 错误: {error_msg}", 
                    exc_info=True)
        
        return Response({
            'success': False,
            'error': error_msg
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sessions(request):
    """列出认证会话
    
    Query Parameters:
        platform_sign: 平台标识（可选）
        account: 账户名（可选）
        status: 会话状态（可选）
        
    Returns:
        会话列表
    """
    logger.info(f"查询会话列表 - 请求用户: {request.user.username}")
    
    try:
        from external_platform.models import AuthSession
        
        # 构建查询条件
        filters = {'is_deleted': False}
        
        platform_sign = request.GET.get('platform_sign')
        if platform_sign:
            filters['platform__sign'] = platform_sign
        
        account = request.GET.get('account')
        if account:
            filters['account'] = account
        
        session_status = request.GET.get('status')
        if session_status:
            filters['status'] = session_status
        
        # 查询会话
        sessions = AuthSession.objects.filter(**filters).select_related('platform')
        
        # 构建响应数据
        session_list = []
        for session in sessions:
            session_info = AuthService.get_session_info(session)
            session_list.append(session_info)
        
        logger.info(f"会话列表查询成功 - 数量: {len(session_list)}")
        
        return Response({
            'success': True,
            'sessions': session_list,
            'count': len(session_list)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        error_msg = f"查询会话列表异常: {str(e)}"
        logger.error(f"会话列表查询异常 - 错误: {error_msg}", exc_info=True)
        
        return Response({
            'success': False,
            'error': error_msg
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_session(request, platform_sign, account):
    """刷新认证会话
    
    Args:
        platform_sign: 平台标识
        account: 账户名
        
    Request Body:
        {
            "password": "password"  # 可选，如果不提供则尝试使用现有凭据
        }
        
    Returns:
        刷新结果
    """
    logger.info(f"刷新认证会话 - 平台: {platform_sign}, 账户: {account}, "
               f"请求用户: {request.user.username}")
    
    try:
        # 获取当前会话
        session = AuthService.get_valid_session(platform_sign, account)
        
        password = request.data.get('password')
        if not password:
            # 如果没有提供密码，尝试从现有会话获取（实际项目中不建议存储明文密码）
            error_msg = "需要提供密码进行会话刷新"
            logger.warning(f"会话刷新缺少密码 - 平台: {platform_sign}, 账户: {account}")
            
            return Response({
                'success': False,
                'error': error_msg
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 触发登录任务进行刷新
        task_id = AuthService.trigger_login_task(platform_sign, account, password)
        
        if task_id:
            logger.info(f"会话刷新任务触发成功 - 任务ID: {task_id}, "
                       f"平台: {platform_sign}, 账户: {account}")
            
            return Response({
                'success': True,
                'task_id': task_id,
                'message': '会话刷新任务已触发'
            }, status=status.HTTP_202_ACCEPTED)
        else:
            error_msg = "触发会话刷新任务失败"
            logger.error(f"会话刷新任务触发失败 - 平台: {platform_sign}, 账户: {account}")
            
            return Response({
                'success': False,
                'error': error_msg
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        error_msg = f"刷新认证会话异常: {str(e)}"
        logger.error(f"会话刷新异常 - 平台: {platform_sign}, 账户: {account}, "
                    f"错误: {error_msg}", exc_info=True)
        
        return Response({
            'success': False,
            'error': error_msg
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)