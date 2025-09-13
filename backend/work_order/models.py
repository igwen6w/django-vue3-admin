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

    version = models.CharField(max_length=32, db_comment='版本', verbose_name='版本', null=True, blank=True, default=None)
    source_system = models.CharField(max_length=36, db_comment='来源标识', verbose_name='来源标识', null=True, blank=True, default=None)
    sync_task_name = models.CharField(max_length=100, db_comment='同步任务名称', verbose_name='同步任务名称', null=True, blank=True, default=None)
    sync_task_id = models.CharField(max_length=36, db_comment='同步任务ID', verbose_name='同步任务ID', null=True, blank=True, default=None)
    sync_status = models.BooleanField(default=False, db_comment='同步状态', verbose_name='同步状态')
    sync_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, db_comment='同步时间', verbose_name='同步时间')
    sync_response = models.JSONField(blank=True, null=True, db_comment='同步响应', verbose_name='同步响应', default=dict)



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
    order_number = models.CharField(max_length=100, blank=True, null=True, db_comment='工单编号', verbose_name='工单编号')
    ps_caption_current = models.CharField(max_length=100, blank=True, null=True, db_comment='当前节点', verbose_name='当前节点')
    order_step_chart = models.JSONField(blank=True, null=True, db_comment='工单节点流程', verbose_name='工单节点流程', default=list)


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

    # 所属分类
    category = models.ManyToManyField('Category', blank=True, db_comment='所属分类', verbose_name='所属分类', related_name='base_work_orders')

    # 所属部门
    department = models.ManyToManyField('system.Dept', blank=True, db_comment='所属部门', verbose_name='所属部门', related_name='base_work_orders')

    # 当前节点
    current_node = models.CharField(max_length=100, blank=True, null=True, db_comment='当前节点', verbose_name='当前节点')
    work_flow = models.JSONField(blank=True, null=True, db_comment='工单流程', verbose_name='工单流程', default=list)

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

    sync_response = models.JSONField(blank=True, null=True, db_comment='同步响应', verbose_name='同步响应', default=dict)
    sync_task_name = models.CharField(max_length=100, db_comment='同步任务名称', verbose_name='同步任务名称', null=True, blank=True)
    sync_task_id = models.CharField(max_length=36, db_comment='同步任务ID', verbose_name='同步任务ID', null=True, blank=True)
    sync_status = models.BooleanField(default=False, db_comment='同步状态', verbose_name='同步状态')
    sync_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, db_comment='同步时间', verbose_name='同步时间')


class Category(CoreModel):
    class Meta:
        db_table = 'work_order_category'
        verbose_name = '工单分类'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    
    name = models.CharField(max_length=100, db_comment='分类名称', verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, db_comment='分类描述', verbose_name='分类描述')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, db_comment='父分类', verbose_name='父分类')


# 办理单位

# 关联记录

# 工单记录

# 附件列表


# 处置
class Disposal(Common):
    class Meta:
        db_table = 'work_order_disposal'
        verbose_name = '处置工单'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    
    base = models.ForeignKey('Base', on_delete=models.CASCADE, db_comment='工单', verbose_name='工单')

    external_id = models.BigIntegerField(default=0, db_comment='工单ID', verbose_name='工单ID')
    # 默认项
    external_ps_caption = models.CharField(max_length=100, db_comment='ps_caption', verbose_name='ps_caption', default='处置')
    external_record_number = models.CharField(max_length=100, db_comment='工单编号', verbose_name='工单编号')
    external_public_record = models.IntegerField(default=2, db_comment='public_record', verbose_name='public_record')
    external_user_id_hide = models.CharField(max_length=100, db_comment='user_id_hide', verbose_name='user_id_hide', null=True, blank=True)
    external_co_di_ids = models.CharField(max_length=100, db_comment='co_di_ids', verbose_name='co_di_ids', null=True, blank=True)
    external_co_di_ids_hide = models.CharField(max_length=100, db_comment='co_di_ids_hide', verbose_name='co_di_ids_hide', null=True, blank=True)
    external_pss_status_attr = models.CharField(max_length=100, db_comment='pss_status_attr', verbose_name='pss_status_attr', default='待处置')
    external_di_ids = models.JSONField(blank=True, null=True, db_comment='单位名称', verbose_name='单位名称', default=list)
    external_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='单位ID', verbose_name='单位ID', default=list)
    external_psot_name = models.CharField(max_length=100, db_comment='psot_name', verbose_name='psot_name', default='处置')
    external_psot_attr = models.CharField(max_length=100, db_comment='psot_attr', verbose_name='psot_attr', default='处置')
    external_pso_caption = models.CharField(max_length=100, db_comment='pso_caption', verbose_name='pso_caption', default='确定')

    # 用户填写项
    external_note1 = models.CharField(max_length=100, db_comment='诉求属实', verbose_name='诉求属实', null=True, blank=True)
    external_distribute_way = models.CharField(max_length=100, db_comment='超职责诉求', verbose_name='超职责诉求', null=True, blank=True)
    external_note8 = models.CharField(max_length=100, db_comment='申请类型', verbose_name='申请类型', null=True, blank=True)
    external_d_attachments = models.JSONField(blank=True, null=True, db_comment='附件', verbose_name='附件', default=list)
    external_note3 = models.CharField(max_length=100, db_comment='联系群众', verbose_name='联系群众', null=True, blank=True)
    external_note4 = models.CharField(max_length=100, db_comment='联系号码', verbose_name='联系号码', null=True, blank=True)
    external_note5 = models.CharField(max_length=100, db_comment='联系时间', verbose_name='联系时间', null=True, blank=True)
    external_note6 = models.CharField(max_length=100, db_comment='是否解决', verbose_name='是否解决', null=True, blank=True)
    external_note11 = models.CharField(max_length=100, db_comment='未解决原因', verbose_name='未解决原因', null=True, blank=True)
    external_note = models.CharField(max_length=100, db_comment='办理情况', verbose_name='办理情况', null=True, blank=True)
    external_note10 = models.CharField(max_length=100, db_comment='公开答复内容', verbose_name='公开答复内容', null=True, blank=True)

    # 附件
    attachments_credentials = models.JSONField(blank=True, null=True, db_comment='证件附件', verbose_name='证件附件', default=list)
    attachments_contact = models.JSONField(blank=True, null=True, db_comment='联系证据', verbose_name='联系证据', default=list)
    attachments_handle = models.JSONField(blank=True, null=True, db_comment='办理附件', verbose_name='办理附件', default=list)


# 下派
class Distribute(Common):
    class Meta:
        db_table = 'work_order_distribute'
        verbose_name = '下派工单'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    
    base = models.ForeignKey('Base', on_delete=models.CASCADE, db_comment='工单', verbose_name='工单')

    external_id = models.BigIntegerField(default=0, db_comment='工单ID', verbose_name='工单ID')
    # 默认项
    external_ps_caption = models.CharField(max_length=100, db_comment='ps_caption', verbose_name='ps_caption', default='处置')
    external_record_number = models.CharField(max_length=100, db_comment='工单编号', verbose_name='工单编号')
    external_public_record = models.IntegerField(default=2, db_comment='public_record', verbose_name='public_record')
    external_user_id_hide = models.CharField(max_length=100, db_comment='user_id_hide', verbose_name='user_id_hide', null=True, blank=True)
    external_co_di_ids = models.JSONField(blank=True, null=True, db_comment='co_di_ids', verbose_name='co_di_ids', default=list)
    external_co_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='co_di_ids_hide', verbose_name='co_di_ids_hide', default=list)
    external_pss_status_attr = models.CharField(max_length=100, db_comment='pss_status_attr', verbose_name='pss_status_attr', default='待处置')
    external_di_ids = models.JSONField(blank=True, null=True, db_comment='单位名称', verbose_name='单位名称', default=list)
    external_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='单位ID', verbose_name='单位ID', default=list)
    external_psot_name = models.CharField(max_length=100, db_comment='psot_name', verbose_name='psot_name', default='加派')
    external_psot_attr = models.CharField(max_length=100, db_comment='psot_attr', verbose_name='psot_attr', default='加派')
    external_pso_caption = models.CharField(max_length=100, db_comment='pso_caption', verbose_name='pso_caption', default='确定')

    # 用户填写项
    external_dept_send_msg = models.CharField(max_length=100, db_comment='单位ID(发短信)', verbose_name='单位ID', null=True, blank=True)
    external_note = models.CharField(max_length=100, db_comment='办理情况', verbose_name='办理情况', null=True, blank=True)
    external_expires = models.IntegerField(default=5, db_comment='办理期限', verbose_name='办理期限')

# 延期

# 退回

# 督办
class Supervise(CoreModel):
    class Meta:
        db_table = 'work_order_supervise'
        verbose_name = '督办工单'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
    
    base = models.ForeignKey('Base', on_delete=models.CASCADE, db_comment='工单', verbose_name='工单')

    # 默认项
    external_ps_caption = models.CharField(max_length=100, db_comment='ps_caption', verbose_name='ps_caption', default='处置')
    external_record_number = models.CharField(max_length=100, db_comment='工单编号', verbose_name='工单编号')
    external_public_record = models.IntegerField(default=2, db_comment='public_record', verbose_name='public_record')
    external_user_id_hide = models.CharField(max_length=100, db_comment='user_id_hide', verbose_name='user_id_hide', null=True, blank=True)
    external_co_di_ids = models.JSONField(blank=True, null=True, db_comment='co_di_ids', verbose_name='co_di_ids', default=list)
    external_co_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='co_di_ids_hide', verbose_name='co_di_ids_hide', default=list)
    external_pss_status_attr = models.CharField(max_length=100, db_comment='pss_status_attr', verbose_name='pss_status_attr', default='待处置')
    external_di_ids = models.JSONField(blank=True, null=True, db_comment='单位名称', verbose_name='单位名称', default=list)
    external_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='单位ID', verbose_name='单位ID', default=list)
    external_psot_name = models.CharField(max_length=100, db_comment='psot_name', verbose_name='psot_name', default='督办')
    external_psot_attr = models.CharField(max_length=100, db_comment='psot_attr', verbose_name='psot_attr', default='督办')
    external_pso_caption = models.CharField(max_length=100, db_comment='pso_caption', verbose_name='pso_caption', default='确定')

    # 用户填写项
    external_note = models.CharField(max_length=100, db_comment='督办意见', verbose_name='督办意见', null=True, blank=True)
    external_refuse_di_ids = models.JSONField(blank=True, null=True, db_comment='督办单位名称', verbose_name='督办单位名称', default=list)
    external_refuse_di_ids_hide = models.JSONField(blank=True, null=True, db_comment='督办单位ID', verbose_name='督办单位ID', default=list)


class DistributeOpinionPreset(CoreModel):
    class Meta:
        db_table = 'work_order_distribute_opinion_preset'
        verbose_name = '下派意见预设'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
        indexes = [
            models.Index(fields=['dept', 'category'], name='dept_category_idx')
        ]
    
    dept = models.ForeignKey('system.Dept', on_delete=models.CASCADE, db_comment='部门', verbose_name='部门')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, db_comment='分类', verbose_name='分类')
    description = models.TextField(blank=True, null=True, db_comment='下派意见预设', verbose_name='下派意见预设')
    title = models.CharField(max_length=100, db_comment='标题', verbose_name='标题', null=True, blank=True)


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

