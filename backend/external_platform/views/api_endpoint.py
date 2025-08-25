from utils.custom_model_viewSet import CustomModelViewSet
from utils.serializers import CustomModelSerializer

from external_platform.models import ApiEndpoint


class ApiEndpointSerializer(CustomModelSerializer):
    class Meta:
        model = ApiEndpoint
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class ApiEndpointViewSet(CustomModelViewSet):
    queryset = ApiEndpoint.objects.filter(is_deleted=False)
    serializer_class = ApiEndpointSerializer