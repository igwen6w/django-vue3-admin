from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from utils.models import CoreModel
from utils.utils import validate_mobile


class WorkOrderSystem(CoreModel):
    """外部工单系统配置"""
    name = models.CharField(max_length=100, db_comment='系统名称', verbose_name='系统名称')
    api_url = models.URLField(max_length=500, db_comment='API地址', verbose_name='API地址')
    api_key = models.CharField(max_length=255, db_comment='API密钥', verbose_name='API密钥')
    username = models.CharField(max_length=100, db_comment='用户名', verbose_name='用户名')
    password = models.CharField(max_length=255, db_comment='密码', verbose_name='密码')
    is_active = models.BooleanField(default=True, db_comment='是否启用', verbose_name='是否启用')
    sync_interval = models.IntegerField(default=300, db_comment='同步间隔(秒)', verbose_name='同步间隔(秒)')
    last_sync_time = models.DateTimeField(null=True, blank=True, db_comment='最后同步时间', verbose_name='最后同步时间')
    
    class Meta:
        db_table = 'work_order_system'
        verbose_name = '工单系统配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class WorkOrder(CoreModel):
    """工单数据模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
        ('cancelled', '已取消'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    # 外部系统信息
    external_system = models.ForeignKey(
        WorkOrderSystem, 
        on_delete=models.CASCADE, 
        db_comment='外部系统', 
        verbose_name='外部系统'
    )
    external_id = models.CharField(max_length=100, db_comment='外部系统ID', verbose_name='外部系统ID')
    
    # 工单基本信息
    title = models.CharField(max_length=200, db_comment='工单标题', verbose_name='工单标题')
    description = models.TextField(db_comment='工单描述', verbose_name='工单描述')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        db_comment='工单状态', 
        verbose_name='工单状态'
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        db_comment='优先级', 
        verbose_name='优先级'
    )
    
    # 相关人员信息
    reporter = models.CharField(max_length=100, db_comment='报告人', verbose_name='报告人')
    assignee = models.CharField(max_length=100, null=True, blank=True, db_comment='负责人', verbose_name='负责人')
    reporter_email = models.EmailField(null=True, blank=True, db_comment='报告人邮箱', verbose_name='报告人邮箱')
    assignee_email = models.EmailField(null=True, blank=True, db_comment='负责人邮箱', verbose_name='负责人邮箱')
    
    # 时间信息
    reported_at = models.DateTimeField(db_comment='报告时间', verbose_name='报告时间')
    due_date = models.DateTimeField(null=True, blank=True, db_comment='截止时间', verbose_name='截止时间')
    resolved_at = models.DateTimeField(null=True, blank=True, db_comment='解决时间', verbose_name='解决时间')
    
    # 分类信息
    category = models.CharField(max_length=100, null=True, blank=True, db_comment='分类', verbose_name='分类')
    tags = models.JSONField(default=list, db_comment='标签', verbose_name='标签')
    
    # 同步信息
    last_sync_at = models.DateTimeField(auto_now=True, db_comment='最后同步时间', verbose_name='最后同步时间')
    sync_status = models.CharField(
        max_length=20, 
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
            ('pending', '待同步'),
        ],
        default='pending',
        db_comment='同步状态', 
        verbose_name='同步状态'
    )
    sync_error = models.TextField(null=True, blank=True, db_comment='同步错误信息', verbose_name='同步错误信息')
    
    class Meta:
        db_table = 'work_order'
        verbose_name = '工单'
        verbose_name_plural = verbose_name
        unique_together = ['external_system', 'external_id']
        indexes = [
            models.Index(fields=['external_system', 'external_id']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['reported_at']),
        ]

    def __str__(self):
        return f"{self.external_system.name} - {self.title}"


class WorkOrderSyncLog(CoreModel):
    """工单同步日志"""
    external_system = models.ForeignKey(
        WorkOrderSystem, 
        on_delete=models.CASCADE, 
        db_comment='外部系统', 
        verbose_name='外部系统'
    )
    sync_type = models.CharField(
        max_length=20,
        choices=[
            ('pull', '拉取'),
            ('update', '更新'),
            ('sync', '同步'),
        ],
        db_comment='同步类型', 
        verbose_name='同步类型'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
            ('partial', '部分成功'),
        ],
        db_comment='执行状态', 
        verbose_name='执行状态'
    )
    total_count = models.IntegerField(default=0, db_comment='总数量', verbose_name='总数量')
    success_count = models.IntegerField(default=0, db_comment='成功数量', verbose_name='成功数量')
    failed_count = models.IntegerField(default=0, db_comment='失败数量', verbose_name='失败数量')
    error_message = models.TextField(null=True, blank=True, db_comment='错误信息', verbose_name='错误信息')
    execution_time = models.FloatField(null=True, blank=True, db_comment='执行时间(秒)', verbose_name='执行时间(秒)')
    
    class Meta:
        db_table = 'work_order_sync_log'
        verbose_name = '工单同步日志'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f"{self.external_system.name} - {self.sync_type} - {self.status}"


class Demo(CoreModel):
    title = models.CharField(max_length=100, db_comment='标题')
    mobile = models.CharField(max_length=15, validators=[validate_mobile], db_comment='手机号')
    sort = models.IntegerField(default=0, db_comment='排序')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'work_order_demo'
        ordering = ['sort']
        verbose_name = '示例'
        verbose_name_plural = verbose_name

    @property
    def full_name(self):
        # return the full name
        return f'{self.first_name} {self.last_name}'

