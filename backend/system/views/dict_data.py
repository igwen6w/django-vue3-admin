from rest_framework import serializers, viewsets
from system.models import DictData
from utils.custom_model_viewSet import CustomModelViewSet


class DictDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = DictData
        fields = '__all__'


class DictDataViewSet(CustomModelViewSet):
    queryset = DictData.objects.filter(is_deleted=False)
    serializer_class = DictDataSerializer
    filterset_fields = ['dict_type']