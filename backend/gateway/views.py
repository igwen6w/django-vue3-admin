import os
import json
import logging
from typing import Dict, Any, Optional

from django.http import JsonResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .api_wrappers import (
    upload_file as api_upload_file
)
from .exceptions import GatewayError, AuthenticationError, PlatformAPIError

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request: Request) -> Response:
    """文件上传API
    
    用户先上传文件到服务器，然后通过平台API转发到远程平台
    """
    try:
        # 检查是否有文件上传
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': '没有找到上传的文件'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        
        # 验证文件
        if uploaded_file.size == 0:
            return JsonResponse({
                'success': False,
                'error': '上传的文件为空'
            }, status=400)
        
        # 获取额外参数
        roll_number = request.data.get('roll_number', '')
        
        # 创建临时文件夹
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        import uuid
        unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
        temp_file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件到服务器磁盘
        try:
            with open(temp_file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            logger.info(f"文件已保存到服务器: {temp_file_path}, 大小: {uploaded_file.size} bytes")
            
            # 准备额外数据
            extra_data = {
                'roll_number': roll_number
            }
            
            # 通过平台API上传到远程平台
            result = api_upload_file(
                file_path=temp_file_path,
                extra_data=extra_data
            )
            
            return JsonResponse({
                'success': True,
                'data': result.get('data'),
                'file_info': {
                    'original_name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'content_type': uploaded_file.content_type,
                    'temp_path': temp_file_path
                }
            })
            
        except Exception as upload_error:
            # 如果上传失败，清理临时文件
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except:
                    pass
            raise upload_error
            
        finally:
            # 上传成功后清理临时文件
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.info(f"临时文件已清理: {temp_file_path}")
                except Exception as cleanup_error:
                    logger.warning(f"清理临时文件失败: {cleanup_error}")
    
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        return JsonResponse({
            'success': False,
            'error': f'文件上传失败: {str(e)}',
            'error_type': 'upload_error'
        }, status=500)

