from external_platform.models import AuthSession
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class AuthSessionSerializer(CustomModelSerializer):
    """
    外部系统鉴权会话 序列化器
    """
    class Meta:
        model = AuthSession
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class AuthSessionFilter(filters.FilterSet):

    class Meta:
        model = AuthSession
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'account', 'status']


class AuthSessionViewSet(CustomModelViewSet):
    """
    外部系统鉴权会话 视图集
    """
    queryset = AuthSession.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = AuthSessionSerializer
    filterset_class = AuthSessionFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
# router.register(r'auth_session', views.AuthSessionViewSet)
# 移入 __init__.py
# from external_platform.views.auth_session import AuthSessionViewSet