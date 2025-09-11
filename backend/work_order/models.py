from django.db import models

from work_order.choices import (
    ExternalSrcWayChoices,
    ExternalNote14Choices,
    ExternalPayrollTypeChoices,
    ExternalProductIdsChoices,
    ExternalAddr2Choices,
    ExternalCompanyAddressChoices,
    ExternalOrderNumberChoices,
    ExternalAddr3Choices,
    ExternalNote1Choices,
    ExternalNote4Choices,
    ExternalHandlingQualityChoices,
    ExternalNote12Choices,
    ExternalNote2Choices,
    ExternalNote3Choices,
    ExternalNote16Choices,
)
from work_order.external.api_endpoint import ApiEndpoint

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
    sync_task_id = models.CharField(max_length=36, db_comment='同步任务ID', verbose_name='同步任务ID')
    sync_status = models.BooleanField(default=False, db_comment='同步状态', verbose_name='同步状态')
    sync_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, db_comment='同步时间', verbose_name='同步时间')



class Meta(Common):
    """ 工单原始信息表, 以 JSON 的形式保存 """
    class Meta:
        db_table = 'work_order_meta'
        verbose_name = '原始工单'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    raw_data = models.JSONField(db_comment='原始工单数据', verbose_name='工单信息', default=dict)
    pull_task_id = models.CharField(max_length=36, db_comment='拉取任务ID', verbose_name='拉取任务ID')
    external_id = models.BigIntegerField(default=0, db_comment='工单ID', verbose_name='工单ID')


class Base(Common):
    """ 工单表, 实际处理工单时需要查看的表, 所有工单信息相关字段和外部工单保持一致 """
    class Meta:
        db_table = 'work_order_base'
        verbose_name = '工单表'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    
    # 基础工单信息
    external_id = models.BigIntegerField(default=0, db_comment='工单ID', verbose_name='工单ID')
    external_roll_number = models.CharField(max_length=100, blank=True, null=True, db_comment='工单编号', verbose_name='工单编号')
    external_handle_rel_expire_time = models.CharField(max_length=50, blank=True, null=True, db_comment='处置实际到期时间', verbose_name='处置实际到期时间')
    external_src_way = models.CharField(max_length=50, choices=ExternalSrcWayChoices.choices, blank=True, null=True, db_comment='受理方式', verbose_name='受理方式')
    external_payroll_name = models.CharField(max_length=100, blank=True, null=True, db_comment='姓名', verbose_name='姓名')
    external_company_tel = models.CharField(max_length=100, blank=True, null=True, db_comment='联系方式', verbose_name='联系方式')
    external_addr = models.CharField(max_length=500, blank=True, null=True, db_comment='地址', verbose_name='地址')
    external_region_district_id = models.CharField(max_length=100, blank=True, null=True, db_comment='区域', verbose_name='区域')
    external_note14 = models.CharField(max_length=50, choices=ExternalNote14Choices.choices, blank=True, null=True, db_comment='是否回访', verbose_name='是否回访')
    external_distribute_way = models.CharField(max_length=200, blank=True, null=True, db_comment='企业名称', verbose_name='企业名称')
    external_payroll_type = models.CharField(max_length=50, choices=ExternalPayrollTypeChoices.choices, blank=True, null=True, db_comment='业务类别', verbose_name='业务类别')
    external_event_type2_id = models.CharField(max_length=200, blank=True, null=True, db_comment='事件类型', verbose_name='事件类型')
    external_roll_content = models.TextField(blank=True, null=True, db_comment='事件描述', verbose_name='事件描述')
    external_note = models.TextField(blank=True, null=True, db_comment='备注', verbose_name='备注')
    
    # 复核相关字段
    external_product_ids = models.CharField(max_length=50, choices=ExternalProductIdsChoices.choices, blank=True, null=True, db_comment='三级复核', verbose_name='三级复核')
    external_addr2 = models.CharField(max_length=50, choices=ExternalAddr2Choices.choices, blank=True, null=True, db_comment='区县复核', verbose_name='区县复核')
    external_company_address = models.CharField(max_length=50, choices=ExternalCompanyAddressChoices.choices, blank=True, null=True, db_comment='满意研判', verbose_name='满意研判')
    external_order_number = models.CharField(max_length=50, choices=ExternalOrderNumberChoices.choices, blank=True, null=True, db_comment='解决研判', verbose_name='解决研判')
    external_normal_payroll_title = models.TextField(blank=True, null=True, db_comment='复核原因', verbose_name='复核原因')
    external_addr3 = models.CharField(max_length=50, choices=ExternalAddr3Choices.choices, blank=True, null=True, db_comment='满意复核', verbose_name='满意复核')
    external_note1 = models.CharField(max_length=100, choices=ExternalNote1Choices.choices, blank=True, null=True, db_comment='解决复核', verbose_name='解决复核')
    external_note15 = models.TextField(blank=True, null=True, db_comment='市复核意见', verbose_name='市复核意见')
    external_attachments = models.JSONField(blank=True, null=True, db_comment='附件', verbose_name='附件')
    
    # 考核和满意度相关字段
    external_note4 = models.CharField(max_length=100, choices=ExternalNote4Choices.choices, blank=True, null=True, db_comment='是否考核', verbose_name='是否考核')
    external_handling_quality = models.CharField(max_length=100, choices=ExternalHandlingQualityChoices.choices, blank=True, null=True, db_comment='办理满意', verbose_name='办理满意')
    external_note12 = models.CharField(max_length=100, choices=ExternalNote12Choices.choices, blank=True, null=True, db_comment='过程满意', verbose_name='过程满意')
    external_note2 = models.CharField(max_length=100, choices=ExternalNote2Choices.choices, blank=True, null=True, db_comment='是否解决', verbose_name='是否解决')
    external_note3 = models.CharField(max_length=100, choices=ExternalNote3Choices.choices, blank=True, null=True, db_comment='办理回复', verbose_name='办理回复')
    external_note16 = models.CharField(max_length=10, choices=ExternalNote16Choices.choices, blank=True, null=True, db_comment='自主研判', verbose_name='自主研判')
    external_note17 = models.TextField(blank=True, null=True, db_comment='研判原因', verbose_name='研判原因')

class BaseEditRecord(CoreModel):
    class Meta:
        db_table = 'work_order_base_edit_record'
        verbose_name = '工单表编辑记录'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
        indexes = [
            models.Index(fields=['external_id']),
        ]
    
    external_id = models.BigIntegerField(default=0, db_comment='工单ID', verbose_name='工单ID')
    act = models.CharField(max_length=50, default='save_payroll_edit', verbose_name='动作标识', db_comment='动作标识')
    external_payroll_result = models.CharField(max_length=50, default='待处置', db_comment='工单状态', verbose_name='工单状态')
    external_roll_number = models.CharField(max_length=100, blank=True, null=True, db_comment='工单编号', verbose_name='工单编号')
    external_product_ids = models.CharField(max_length=50, choices=ExternalProductIdsChoices.choices, blank=True, null=True, db_comment='三级复核', verbose_name='三级复核')
    external_addr2 = models.CharField(max_length=50, choices=ExternalAddr2Choices.choices, blank=True, null=True, db_comment='区县复核', verbose_name='区县复核')
    external_company_address = models.CharField(max_length=50, choices=ExternalCompanyAddressChoices.choices, blank=True, null=True, db_comment='满意研判', verbose_name='满意研判')
    external_order_number = models.CharField(max_length=50, choices=ExternalOrderNumberChoices.choices, blank=True, null=True, db_comment='解决研判', verbose_name='解决研判')
    external_normal_payroll_title = models.TextField(blank=True, null=True, db_comment='复核原因', verbose_name='复核原因')
    external_note16 = models.CharField(max_length=50, choices=ExternalNote16Choices.choices, blank=True, null=True, db_comment='自主研判', verbose_name='自主研判')
    external_note17 = models.TextField(blank=True, null=True, db_comment='研判原因', verbose_name='研判原因')

    sync_task_id = models.CharField(max_length=36, db_comment='同步任务ID', verbose_name='同步任务ID', null=True, blank=True)
    sync_status = models.BooleanField(default=False, db_comment='同步状态', verbose_name='同步状态')
    sync_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, db_comment='同步时间', verbose_name='同步时间')


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


class Demo(CoreModel):
    title = models.CharField(max_length=100, default='', db_comment='标题')
    mobile = models.CharField(max_length=15, default='', validators=[validate_mobile], db_comment='手机号')
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

