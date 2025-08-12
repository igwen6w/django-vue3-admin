from utils.custom_model_viewSet import CustomModelViewSet
from utils.serializers import CustomModelSerializer

from work_order.models import Demo


class DemoSerializer(CustomModelSerializer):
    class Meta:
        model = Demo
        fields = '__all__'
        read_only_fields = ['id', 'create_time']


class DemoViewSet(CustomModelViewSet):
    queryset = Demo.objects.filter(is_deleted=False)
    serializer_class = DemoSerializer