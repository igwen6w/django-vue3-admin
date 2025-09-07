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
    AuthStatusResponseSerializer, LoginRequestSerializer
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

