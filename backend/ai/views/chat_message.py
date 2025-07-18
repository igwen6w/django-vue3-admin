from rest_framework import serializers

from ai.models import ChatMessage
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class ChatMessageSerializer(CustomModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    """
    AI 聊天消息 序列化器
    """
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']


class ChatMessageFilter(filters.FilterSet):

    class Meta:
        model = ChatMessage
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'conversation_id',
                  'model', 'type', 'reply_id', 'content', 'use_context', 'segment_ids']


class ChatMessageViewSet(CustomModelViewSet):
    """
    AI 聊天消息 视图集
    """
    queryset = ChatMessage.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ChatMessageSerializer
    filterset_class = ChatMessageFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

