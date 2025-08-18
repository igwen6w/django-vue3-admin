from django.db import models

from utils.models import CoreModel
from utils.utils import validate_mobile


class Common(CoreModel):
    """ 原始工单和工单表中公共存在的一部分数据 """
    class Meta:
        abstract = True
        verbose_name = '工单公共部分'
        verbose_name_plural = verbose_name

    version = models.CharField(max_length=32, db_comment='版本', verbose_name='版本')
    source_system = models.CharField(max_length=20, db_comment='来源标识', verbose_name='来源标识')
    sync_task_id = models.BigIntegerField(db_comment='同步任务ID', verbose_name='同步任务ID')
    sync_status = models.BooleanField(default=False, db_comment='同步状态', verbose_name='同步状态')
    sync_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, db_comment='同步时间', verbose_name='同步时间')



class Meta(Common):
    """ 工单原始信息表, 以 JSON 的形式保存 """
    class Meta:
        db_table = 'work_order_meta'
        verbose_name = '原始工单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    raw_data = models.JSONField(db_commnet='原始工单数据', verbose_name='工单信息')
    pull_task_id = models.BigIntegerField(db_comment='拉取任务ID', verbose_name='拉取任务ID')


class Base(Common):
    """ 工单表, 实际处理工单时需要查看的表, 所有工单信息相关字段和外部工单保持一致 """
    class Meta:
        db_table = 'work_order_base'
        verbose_name = '工单表'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    ...


# 办理单位

# 关联记录

# 工单记录

# 附件列表

# 工作流程

# 处置

# 下派

# 延期

# 退回

# 督办

# 外部工单系统

class ExternalAuthSession(CoreModel):
    class Meta:
        db_table = 'external_auth_session'
        ordering = ['update_time']
        verbose_name = '外部系统鉴权会话'
        verbose_name_plural = verbose_name
    
    pass

class ExternalApiLog(CoreModel):
    class Meta:
        db_table = 'external_api_log'
        ordering = ['create_time']
        verbose_name = '外部系统API端点访问日志'
        verbose_name_plural = verbose_name
    
    pass

class ExternalAuthCaptchaLog(CoreModel):
    class Meta:
        db_table = 'external_auth_captcha_log'
        ordering = ['create_time']
        verbose_name = '外部系统验证码识别结果日志'
        verbose_name_plural = verbose_name
    pass

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

