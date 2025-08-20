from django.db import models


class ExternalSrcWayChoices(models.TextChoices):
    """受理方式选择"""
    TEL = '电话', '电话'
    WEBSITE = '网站', '网站'
    WEIBO = '微博', '微博'
    WECHAT = '微信', '微信'
    AISHANDONG_APP = '爱山东APP', '爱山东APP'
    EMAIL = '电子信箱', '电子信箱'
    PROVINCE_PLATFORM = '省平台', '省平台'
    COMPLAINT_RESPONSE = '接诉即办', '接诉即办'
    PROVINCE_WEBSITE = '省网站', '省网站'
    ENTERPRISE_SPECIALIST = '企业专员', '企业专员'
    GOVERNMENT_INTERACTION = '政民互动', '政民互动'
    CITY_110 = '市110', '市110'
    LIGHTNING_NEWS = '闪电新闻', '闪电新闻'
    ENTERPRISE_MAYOR_HOTLINE = '企业市长直通车', '企业市长直通车'


class ExternalNote14Choices(models.TextChoices):
    """是否回访选择"""
    EMPTY = '', ''
    CALLBACK = '回访', '回访'
    NO_CALLBACK = '不回访', '不回访'


class ExternalPayrollTypeChoices(models.TextChoices):
    """业务类别选择"""
    HELP = '求助', '求助'
    CONSULTATION = '咨询', '咨询'
    COMPLAINT = '投诉', '投诉'
    REPORT = '举报', '举报'
    SUGGESTION = '建议', '建议'
    THANKS = '感谢', '感谢'
    CANCEL = '撤单', '撤单'
    HARASSMENT = '骚扰', '骚扰'
    INVALID = '无效', '无效'


class ExternalProductIdsChoices(models.TextChoices):
    """三级复核选择"""
    EMPTY = '', ''
    APPLY_REVIEW = '申请复核', '申请复核'
    PASS = '通过', '通过'
    NOT_PASS = '不通过', '不通过'


class ExternalAddr2Choices(models.TextChoices):
    """区县复核选择"""
    EMPTY = '', ''
    APPLY_REVIEW = '申请复核', '申请复核'
    PASS = '通过', '通过'
    NOT_PASS = '不通过', '不通过'


class ExternalCompanyAddressChoices(models.TextChoices):
    """满意研判选择"""
    EMPTY = '', ''
    REVIEW_PASS = '复核通过', '复核通过'
    OUT_OF_SCOPE = '超职责范围', '超职责范围'


class ExternalOrderNumberChoices(models.TextChoices):
    """解决研判选择"""
    EMPTY = '', ''
    REVIEW_PASS = '复核通过', '复核通过'
    OUT_OF_SCOPE = '超职责范围', '超职责范围'


class ExternalAddr3Choices(models.TextChoices):
    """满意复核选择"""
    EMPTY = '', ''
    PENDING_REVIEW = '待复核', '待复核'
    NO_ANSWER_1 = '未接通1', '未接通1'
    NO_ANSWER_2 = '未接通2', '未接通2'
    REVIEW_COMPLETED = '复核完成', '复核完成'
    REVIEW_PASS = '复核通过', '复核通过'
    REVIEW_NOT_PASS = '复核不通过', '复核不通过'
    OUT_OF_SCOPE_PASS = '不在范围通过', '不在范围通过'
    CANCEL_PASS = '撤单通过', '撤单通过'


class ExternalNote1Choices(models.TextChoices):
    """解决复核选择"""
    EMPTY = '', ''
    PENDING_REVIEW = '待复核', '待复核'
    NO_ANSWER_1 = '未接通1', '未接通1'
    NO_ANSWER_2 = '未接通2', '未接通2'
    REVIEW_COMPLETED = '复核完成', '复核完成'
    RESOLVED = '解决', '解决'
    BASICALLY_RESOLVED = '基本解决', '基本解决'
    OUT_OF_SCOPE_PASS = '不在范围通过', '不在范围通过'


class ExternalNote4Choices(models.TextChoices):
    """是否考核选择"""
    EMPTY = '', ''
    INCLUDE_ASSESSMENT = '计入考核', '计入考核'
    NOT_INCLUDE_ASSESSMENT = '不计入考核', '不计入考核'
    REASONABLE_DEMAND = '合理诉求', '合理诉求'
    UNREASONABLE_DEMAND = '不合理诉求', '不合理诉求'


class ExternalHandlingQualityChoices(models.TextChoices):
    """办理满意选择"""
    EMPTY = '', ''
    SATISFIED = '满意', '满意'
    BASICALLY_SATISFIED = '基本满意', '基本满意'
    DISSATISFIED = '不满意', '不满意'
    UNABLE_TO_CALLBACK = '无法回访', '无法回访'
    NO_ANSWER = '无人接听', '无人接听'


class ExternalNote12Choices(models.TextChoices):
    """过程满意选择"""
    EMPTY = '', ''
    SATISFIED = '满意', '满意'
    BASICALLY_SATISFIED = '基本满意', '基本满意'
    DISSATISFIED = '不满意', '不满意'


class ExternalNote2Choices(models.TextChoices):
    """是否解决选择"""
    EMPTY = '', ''
    RESOLVED = '解决', '解决'
    BASICALLY_RESOLVED = '基本解决', '基本解决'
    NOT_RESOLVED = '未解决', '未解决'
    COMPLETED = '办成', '办成'
    NOT_COMPLETED = '未办成', '未办成'


class ExternalNote3Choices(models.TextChoices):
    """办理回复选择"""
    EMPTY = '', ''
    REPLIED = '回复', '回复'
    NOT_REPLIED = '未回复', '未回复'


class ExternalNote16Choices(models.TextChoices):
    """自主研判选择"""
    EMPTY = '', ''
    YES = '是', '是'
    NO = '否', '否'