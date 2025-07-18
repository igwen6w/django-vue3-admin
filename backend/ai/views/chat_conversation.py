from rest_framework import serializers

from ai.models import ChatConversation
from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet
from django_filters import rest_framework as filters


class ChatConversationSerializer(CustomModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    """
    AI 聊天对话 序列化器
    """
    class Meta:
        model = ChatConversation
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']

class ChatConversationFilter(filters.FilterSet):

    class Meta:
        model = ChatConversation
        fields = ['id', 'remark', 'creator', 'modifier', 'is_deleted', 'title', 'pinned', 'model',
                  'system_message', 'max_tokens', 'max_contexts']


class ChatConversationViewSet(CustomModelViewSet):
    """
    AI 聊天对话 视图集
    """
    queryset = ChatConversation.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ChatConversationSerializer
    filterset_class = ChatConversationFilter
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']

# 移入urls中
