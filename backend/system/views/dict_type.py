from rest_framework import serializers, viewsets
from system.models import DictType
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class DictTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DictType
        fields = '__all__'


class DictTypeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    value = filters.CharFilter(field_name='value', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = DictType
        fields = ['name', 'value', 'status']


class DictTypeViewSet(CustomModelViewSet):
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer
    filterset_class = DictTypeFilter
    search_fields = ['name', 'type']
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']