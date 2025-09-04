from utils.custom_model_viewSet import CustomModelViewSet
from utils.serializers import CustomModelSerializer

from external_platform.models import Platform, AuthSession, PlatformEndpoint, PlatformConfig, RequestLog


class PlatformSerializer(CustomModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class PlatformViewSet(CustomModelViewSet):
    queryset = Platform.objects.filter(is_deleted=False)
    serializer_class = PlatformSerializer
    enable_soft_delete = True


class AuthSessionSerializer(CustomModelSerializer):
    class Meta:
        model = AuthSession
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class AuthSessionViewSet(CustomModelViewSet):
    queryset = AuthSession.objects.filter(is_deleted=False)
    serializer_class = AuthSessionSerializer
    enable_soft_delete = True


class PlatformEndpointSerializer(CustomModelSerializer):
    class Meta:
        model = PlatformEndpoint
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class PlatformEndpointViewSet(CustomModelViewSet):
    queryset = PlatformEndpoint.objects.filter(is_deleted=False)
    serializer_class = PlatformEndpointSerializer
    enable_soft_delete = True


class PlatformConfigSerializer(CustomModelSerializer):
    class Meta:
        model = PlatformConfig
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class PlatformConfigViewSet(CustomModelViewSet):
    queryset = PlatformConfig.objects.filter(is_deleted=False)
    serializer_class = PlatformConfigSerializer
    enable_soft_delete = True


class RequestLogSerializer(CustomModelSerializer):
    class Meta:
        model = RequestLog
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class RequestLogViewSet(CustomModelViewSet):
    queryset = RequestLog.objects.filter(is_deleted=False)
    serializer_class = RequestLogSerializer
    enable_soft_delete = True