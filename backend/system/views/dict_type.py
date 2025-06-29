from rest_framework import serializers, viewsets
from system.models import DictType
from utils.custom_model_viewSet import CustomModelViewSet


class DictTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DictType
        fields = '__all__'


class DictTypeViewSet(CustomModelViewSet):
    queryset = DictType.objects.filter(is_deleted=False)
    serializer_class = DictTypeSerializer