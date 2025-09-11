import logging
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from external_platform.models import Platform, AuthSession
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters

logger = logging.getLogger(__name__)


class PlatformSerializer(CustomModelSerializer):
    """
    外部平台 序列化器
    """
    class Meta:
        model = Platform
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']

class LoginRequestSerializer(serializers.Serializer):
    """
    登录请求序列化器
    """
    platform_sign = serializers.CharField(
        max_length=100,
        help_text="平台标识",
        error_messages={
            'required': '平台标识不能为空',
            'max_length': '平台标识长度不能超过100个字符'
        }
    )
    
    account = serializers.CharField(
        max_length=100,
        help_text="账户名",
        error_messages={
            'required': '账户名不能为空',
            'max_length': '账户名长度不能超过100个字符'
        }
    )
    
    password = serializers.CharField(
        max_length=200,
        help_text="密码",
        style={'input_type': 'password'},
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不能超过200个字符'
        }
    )
    
    def validate_platform_sign(self, value):
        """验证平台标识是否存在"""
        try:
            Platform.objects.get(sign=value, is_active=True, is_deleted=False)
        except Platform.DoesNotExist:
            raise serializers.ValidationError("指定的平台不存在或未激活")
        return value


class AuthStatusResponseSerializer(serializers.Serializer):
    """
    认证状态响应序列化器
    """
    success = serializers.BooleanField(help_text="是否成功")
    authenticated = serializers.BooleanField(help_text="是否已认证")
    session = serializers.DictField(help_text="会话信息", required=False)
    message = serializers.CharField(max_length=200, help_text="响应消息", required=False)
    error = serializers.CharField(max_length=500, help_text="错误信息", required=False)


class PlatformFilter(filters.FilterSet):

    class Meta:
        model = Platform
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'name', 'sign', 'base_url', 'captcha_type', 'session_timeout_hours', 'retry_limit', 'is_active']


class PlatformViewSet(CustomModelViewSet):
    """
    外部平台 视图集
    """
    queryset = Platform.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = PlatformSerializer
    filterset_class = PlatformFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']


# 移入urls中
# router.register(r'platform', views.PlatformViewSet)
# 移入 __init__.py
# from external_platform.views.platform import PlatformViewSet, PlatformLogin