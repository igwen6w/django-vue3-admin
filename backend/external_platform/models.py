from django.db import models

from common.fields import EncryptedTextField
from external_platform.choices import PlatformAuthStatus, ApiMethod

from utils.models import CoreModel

class Platform(CoreModel):
    class Meta:
        db_table = 'external_platform'
        verbose_name = '外部平台'
        verbose_name_plural = verbose_name
        unique_together = [
            ['sign']
        ]
    
    name = models.CharField(db_comment='名称', max_length=100)
    sign = models.CharField(db_comment='标识', max_length=50, unique=True)
    base_url = models.URLField(db_comment='基础URL', max_length=200)
    captcha_type = models.IntegerField(db_comment='验证码类型', default=1004, help_text='超级鹰验证码类型')
    session_timeout_hours = models.IntegerField(db_comment='会话超时时间(小时)', default=24)
    retry_limit = models.IntegerField(db_comment='重试次数限制', default=3)
    is_active = models.BooleanField(db_comment='是否启用', default=True)
    description = models.TextField(db_comment='平台描述', null=True, blank=True)
    login_config = EncryptedTextField(db_comment='登录配置(json 加密)', verbose_name='登录配置', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}({self.sign})"

class AuthSession(CoreModel):
    class Meta:
        db_table = 'external_auth_session'
        ordering = ['update_time']
        verbose_name = '外部系统鉴权会话'
        verbose_name_plural = verbose_name
        unique_together = [['platform', 'account']]

    platform = models.ForeignKey(
        Platform, 
        db_comment='关联外部平台',
        verbose_name='外部平台', 
        on_delete=models.CASCADE,
        db_column='external_platform_id'
    )
    account = models.CharField(verbose_name='账号', max_length=50)
    auth = models.JSONField(verbose_name='鉴权信息', null=True, blank=True)
    status = models.CharField(
        verbose_name='鉴权状态', 
        max_length=50, 
        choices=PlatformAuthStatus.choices, 
        default=PlatformAuthStatus.EXPIRED
    )
    expire_time = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="过期时间",
        verbose_name="过期时间"
    )
    login_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name = '登录时间'
    )
    
class PlatformEndpoint(CoreModel):
    """平台端点配置"""
    class Meta:
        db_table = 'external_platform_endpoint'
        verbose_name = '平台端点配置'
        verbose_name_plural = verbose_name
        unique_together = [
            ['platform', 'endpoint_type']
        ]
    
    ENDPOINT_TYPES = [
        ('captcha', '验证码'),
        ('login', '登录'),
        ('check_status', '状态检查'),
        ('workorder_list', '工单列表'),
        ('workorder_detail', '工单详情'),
        ('workorder_related_record', '工单关联'),
        ('workorder_work_unit_record', '工单办理单位'),
        ('workorder_poerate_record', '工单办理单位'),
        ('workorder_attachment_record', '工单附件'),
        ('workorder_flow_record', '工单流程'),
        ('workorder_action_edit', '编辑工单'),
        ('workorder_action_disposal', '处置工单'),
        ('workorder_action_send', '下派工单'),
        ('workorder_action_back', '退回工单'),
        ('workorder_action_postpone', '延期工单'),
        ('workorder_action_supervise', '督办工单'),
        ('logout', '登出'),
        ('custom', '自定义'),
    ]
    
    platform = models.ForeignKey(
        Platform,
        verbose_name='外部平台',
        on_delete=models.CASCADE,
        db_column='external_platform_id'
    )
    endpoint_type = models.CharField(
        verbose_name='端点类型',
        max_length=50,
        choices=ENDPOINT_TYPES
    )
    name = models.CharField(verbose_name='端点名称', max_length=100, null=True, blank=True)
    path = models.CharField(verbose_name='路径', max_length=200)
    http_method = models.CharField(
        verbose_name='请求方式',
        max_length=10,
        choices=ApiMethod.choices,
        default=ApiMethod.GET
    )
    require_auth = models.BooleanField(verbose_name='是否需要鉴权', default=False)
    description = models.TextField(verbose_name='端点说明', null=True, blank=True)
    payload = models.JSONField(verbose_name='载荷', null=True, blank=True, default=dict)
    
    def __str__(self):
        if self.name:
            return f"{self.platform.name} - {self.name}"
        return f"{self.platform.name} - {self.get_endpoint_type_display()}"


class PlatformConfig(CoreModel):
    """平台额外配置"""
    class Meta:
        db_table = 'external_platform_config'
        verbose_name = '平台配置'
        verbose_name_plural = verbose_name
        unique_together = [
            ['platform', 'config_key']
        ]
    
    platform = models.ForeignKey(
        Platform,
        verbose_name='外部平台',
        on_delete=models.CASCADE,
        db_column='external_platform_id'
    )
    config_key = models.CharField(verbose_name='配置键', max_length=100)
    config_value = models.JSONField(verbose_name='配置值')
    description = models.TextField(verbose_name='配置说明', null=True, blank=True)
    
    def __str__(self):
        return f"{self.platform.name} - {self.config_key}"




class RequestLog(CoreModel):
    class Meta:
        db_table = 'external_request_log'
        ordering = ['create_time']
        verbose_name = '外部系统请求日志'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['platform', 'create_time']),
            models.Index(fields=['endpoint_path', 'status_code']),
            models.Index(fields=['account', 'create_time'])
        ]

    platform = models.ForeignKey(
        Platform, 
        db_comment='关联外部平台',
        verbose_name='外部平台', 
        on_delete=models.CASCADE,
        db_column='external_platform_id'
    )
    platform_endpoint = models.ForeignKey(
        PlatformEndpoint, 
        verbose_name='平台端点', 
        on_delete=models.CASCADE,
        db_column='external_platform_endpoint_id',
        null=True,
        blank=True
    )
    account = models.CharField(verbose_name='账号', max_length=50)
    endpoint_path = models.CharField(max_length=255, verbose_name='端点路径')
    method = models.CharField(
        max_length=10, 
        verbose_name='方法', 
        choices=ApiMethod.choices,
        default=ApiMethod.GET
    )
    payload = models.JSONField(null=True, verbose_name='请求参数')
    status_code = models.IntegerField(default=200, verbose_name='响应状态码')
    response_time_ms = models.IntegerField(default=0, verbose_name='响应耗时')
    response_body = models.JSONField(null=True, blank=True, verbose_name='响应体')
    hook = models.JSONField(null=True, blank=True, verbose_name='请求后钩子')
    hook_result = models.JSONField(null=True, blank=True, verbose_name='钩子结果')
    error_message = models.TextField(null=True, blank=True, verbose_name='请求错误消息')
    tag = models.JSONField(verbose_name='标签', null=True, blank=True)

class ExternalAuthCaptchaLog(CoreModel):
    class Meta:
        db_table = 'external_auth_captcha_log'
        ordering = ['create_time']
        verbose_name = '外部系统验证码识别结果日志'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['request_log'], name='request_log_id_idx')
        ]
    
    request_log = models.ForeignKey(
        RequestLog, 
        verbose_name='请求记录', 
        on_delete=models.CASCADE,
        db_column='external_request_log_id'
    )

class ExternalDistrictNode(CoreModel):
    class Meta:
        db_table = 'external_district_node'
        verbose_name = '区县节点'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
        indexes = [
            models.Index(fields=['code'], name='code_idx')
        ]
    
    name = models.CharField(max_length=100, db_comment='名称', verbose_name='名称')
    code = models.CharField(max_length=10, db_comment='编码', verbose_name='编码', unique=True)
    parent = models.ForeignKey(
        'self', 
        to_field='code', 
        on_delete=models.CASCADE, 
        db_comment='父节点', 
        verbose_name='父节点', 
        related_name='children',
        null=True,
        blank=True
    )