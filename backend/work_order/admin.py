"""
工单模块管理界面配置
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import WorkOrderSystem, WorkOrder, WorkOrderSyncLog


@admin.register(WorkOrderSystem)
class WorkOrderSystemAdmin(admin.ModelAdmin):
    """工单系统配置管理"""
    list_display = [
        'name', 'api_url', 'is_active', 'sync_interval', 
        'last_sync_time', 'create_time', 'update_time'
    ]
    list_filter = ['is_active', 'create_time', 'update_time']
    search_fields = ['name', 'api_url']
    readonly_fields = ['last_sync_time', 'create_time', 'update_time']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'api_url', 'is_active')
        }),
        ('认证信息', {
            'fields': ('api_key', 'username', 'password'),
            'classes': ('collapse',)
        }),
        ('同步配置', {
            'fields': ('sync_interval', 'last_sync_time')
        }),
        ('系统信息', {
            'fields': ('create_time', 'update_time', 'creator', 'modifier', 'remark'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """创建时某些字段可编辑，编辑时只读"""
        if obj:  # 编辑模式
            return self.readonly_fields + ('name',)
        return self.readonly_fields


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    """工单管理"""
    list_display = [
        'external_id', 'title', 'external_system', 'status', 'priority',
        'reporter', 'assignee', 'reported_at', 'due_date', 'sync_status'
    ]
    list_filter = [
        'status', 'priority', 'external_system', 'sync_status',
        'reported_at', 'due_date', 'create_time'
    ]
    search_fields = [
        'external_id', 'title', 'description', 'reporter', 'assignee'
    ]
    readonly_fields = [
        'external_system', 'external_id', 'sync_status', 'sync_error',
        'last_sync_at', 'create_time', 'update_time'
    ]
    
    fieldsets = (
        ('外部系统信息', {
            'fields': ('external_system', 'external_id', 'sync_status', 'sync_error')
        }),
        ('工单基本信息', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('相关人员', {
            'fields': ('reporter', 'reporter_email', 'assignee', 'assignee_email')
        }),
        ('时间信息', {
            'fields': ('reported_at', 'due_date', 'resolved_at')
        }),
        ('分类信息', {
            'fields': ('category', 'tags')
        }),
        ('系统信息', {
            'fields': ('last_sync_at', 'create_time', 'update_time', 'creator', 'modifier', 'remark'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('external_system')
    
    def status_color(self, obj):
        """状态颜色显示"""
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'resolved': 'green',
            'closed': 'gray',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_color.short_description = '状态'
    
    def priority_color(self, obj):
        """优先级颜色显示"""
        colors = {
            'low': 'green',
            'medium': 'blue',
            'high': 'orange',
            'urgent': 'red',
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_color.short_description = '优先级'


@admin.register(WorkOrderSyncLog)
class WorkOrderSyncLogAdmin(admin.ModelAdmin):
    """工单同步日志管理"""
    list_display = [
        'external_system', 'sync_type', 'status', 'total_count',
        'success_count', 'failed_count', 'execution_time', 'create_time'
    ]
    list_filter = [
        'external_system', 'sync_type', 'status', 'create_time'
    ]
    search_fields = ['external_system__name']
    readonly_fields = [
        'external_system', 'sync_type', 'status', 'total_count',
        'success_count', 'failed_count', 'error_message', 'execution_time',
        'create_time', 'update_time'
    ]
    
    fieldsets = (
        ('同步信息', {
            'fields': ('external_system', 'sync_type', 'status')
        }),
        ('执行结果', {
            'fields': ('total_count', 'success_count', 'failed_count', 'execution_time')
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('create_time', 'update_time', 'creator', 'modifier', 'remark'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('external_system')
    
    def has_add_permission(self, request):
        """禁止手动添加同步日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改同步日志"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """允许删除同步日志"""
        return True
    
    def status_color(self, obj):
        """状态颜色显示"""
        colors = {
            'success': 'green',
            'failed': 'red',
            'partial': 'orange',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_color.short_description = '状态'
    
    def execution_time_display(self, obj):
        """执行时间显示"""
        if obj.execution_time:
            return f"{obj.execution_time:.2f}秒"
        return "-"
    execution_time_display.short_description = '执行时间'


# 自定义管理站点标题
admin.site.site_header = "工单管理系统"
admin.site.site_title = "工单管理"
admin.site.index_title = "工单管理后台"
