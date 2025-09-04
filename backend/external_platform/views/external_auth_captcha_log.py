from external_platform.models import ExternalAuthCaptchaLog
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class ExternalAuthCaptchaLogSerializer(CustomModelSerializer):
    """
    外部系统验证码识别结果日志 序列化器
    """
    class Meta:
        model = ExternalAuthCaptchaLog
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ExternalAuthCaptchaLogFilter(filters.FilterSet):

    class Meta:
        model = ExternalAuthCaptchaLog
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted']


class ExternalAuthCaptchaLogViewSet(CustomModelViewSet):
    """
    外部系统验证码识别结果日志 视图集
    """
    queryset = ExternalAuthCaptchaLog.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ExternalAuthCaptchaLogSerializer
    filterset_class = ExternalAuthCaptchaLogFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'external_auth_captcha_log', views.ExternalAuthCaptchaLogViewSet)
# 移入 __init__.py
# from external_platform.views.external_auth_captcha_log import ExternalAuthCaptchaLogViewSet