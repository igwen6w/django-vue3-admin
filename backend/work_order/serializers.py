"""
工单序列化器
"""
from rest_framework import serializers
from .models import WorkOrderSystem, WorkOrder, WorkOrderSyncLog


class WorkOrderSystemSerializer(serializers.ModelSerializer):
    """工单系统配置序列化器"""
    
    class Meta:
        model = WorkOrderSystem
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # 密码字段不返回
            'api_key': {'write_only': True},   # API密钥不返回
        }
    
    def to_representation(self, instance):
        """自定义返回格式，隐藏敏感信息"""
        data = super().to_representation(instance)
        # 隐藏敏感信息
        data['password'] = '***' if instance.password else ''
        data['api_key'] = '***' if instance.api_key else ''
        return data


class WorkOrderSerializer(serializers.ModelSerializer):
    """工单序列化器"""
    
    external_system_name = serializers.CharField(source='external_system.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ['external_system', 'external_id', 'sync_status', 'sync_error', 'last_sync_at']


class WorkOrderSyncLogSerializer(serializers.ModelSerializer):
    """工单同步日志序列化器"""
    
    external_system_name = serializers.CharField(source='external_system.name', read_only=True)
    sync_type_display = serializers.CharField(source='get_sync_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = WorkOrderSyncLog
        fields = '__all__'
        read_only_fields = ['external_system', 'sync_type', 'status', 'total_count', 
                           'success_count', 'failed_count', 'error_message', 'execution_time']


class WorkOrderUpdateSerializer(serializers.ModelSerializer):
    """工单更新序列化器"""
    
    class Meta:
        model = WorkOrder
        fields = ['title', 'description', 'status', 'priority', 'assignee', 
                 'assignee_email', 'due_date', 'category', 'tags']
    
    def validate_status(self, value):
        """验证状态值"""
        valid_statuses = [choice[0] for choice in WorkOrder.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"无效的状态值: {value}")
        return value
    
    def validate_priority(self, value):
        """验证优先级值"""
        valid_priorities = [choice[0] for choice in WorkOrder.PRIORITY_CHOICES]
        if value not in valid_priorities:
            raise serializers.ValidationError(f"无效的优先级值: {value}")
        return value


class WorkOrderSystemCreateSerializer(serializers.ModelSerializer):
    """工单系统创建序列化器"""
    
    class Meta:
        model = WorkOrderSystem
        fields = ['name', 'api_url', 'api_key', 'username', 'password', 
                 'is_active', 'sync_interval']
    
    def validate_name(self, value):
        """验证系统名称"""
        # 检查名称是否已存在
        if WorkOrderSystem.objects.filter(name=value).exists():
            raise serializers.ValidationError("系统名称已存在")
        return value
    
    def validate_api_url(self, value):
        """验证API URL"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("API URL必须以http://或https://开头")
        return value
    
    def validate_sync_interval(self, value):
        """验证同步间隔"""
        if value < 60:  # 最少1分钟
            raise serializers.ValidationError("同步间隔不能少于60秒")
        if value > 86400:  # 最多24小时
            raise serializers.ValidationError("同步间隔不能超过86400秒（24小时）")
        return value


class WorkOrderSystemUpdateSerializer(serializers.ModelSerializer):
    """工单系统更新序列化器"""
    
    class Meta:
        model = WorkOrderSystem
        fields = ['name', 'api_url', 'api_key', 'username', 'password', 
                 'is_active', 'sync_interval']
    
    def validate_name(self, value):
        """验证系统名称"""
        # 检查名称是否已存在（排除当前实例）
        instance = self.instance
        if instance and WorkOrderSystem.objects.filter(name=value).exclude(id=instance.id).exists():
            raise serializers.ValidationError("系统名称已存在")
        return value
    
    def validate_api_url(self, value):
        """验证API URL"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("API URL必须以http://或https://开头")
        return value
    
    def validate_sync_interval(self, value):
        """验证同步间隔"""
        if value < 60:  # 最少1分钟
            raise serializers.ValidationError("同步间隔不能少于60秒")
        if value > 86400:  # 最多24小时
            raise serializers.ValidationError("同步间隔不能超过86400秒（24小时）")
        return value


class SyncTaskResultSerializer(serializers.Serializer):
    """同步任务结果序列化器"""
    task_id = serializers.CharField(help_text="任务ID")
    status = serializers.CharField(help_text="任务状态")
    result = serializers.DictField(help_text="任务结果", required=False)
    error = serializers.CharField(help_text="错误信息", required=False)


class WorkOrderStatisticsSerializer(serializers.Serializer):
    """工单统计序列化器"""
    total_count = serializers.IntegerField(help_text="总工单数")
    pending_count = serializers.IntegerField(help_text="待处理工单数")
    processing_count = serializers.IntegerField(help_text="处理中工单数")
    resolved_count = serializers.IntegerField(help_text="已解决工单数")
    closed_count = serializers.IntegerField(help_text="已关闭工单数")
    cancelled_count = serializers.IntegerField(help_text="已取消工单数")
    
    # 按优先级统计
    low_priority_count = serializers.IntegerField(help_text="低优先级工单数")
    medium_priority_count = serializers.IntegerField(help_text="中优先级工单数")
    high_priority_count = serializers.IntegerField(help_text="高优先级工单数")
    urgent_priority_count = serializers.IntegerField(help_text="紧急优先级工单数")
    
    # 按系统统计
    system_stats = serializers.DictField(help_text="按系统统计的工单数")
