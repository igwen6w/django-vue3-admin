from django.db import models

from ai.choices import PlatformChoices
from utils.models import CommonStatus, CoreModel

class AIApiKey(CoreModel):
    """ AI API 密钥表 """
    name = models.CharField(max_length=255, db_comment="名称", verbose_name="名称")
    platform = models.CharField(
        max_length=100,
        choices=PlatformChoices.choices,
        verbose_name="平台",
        db_comment="平台"
    )
    api_key = models.CharField(max_length=255, db_comment="密钥", verbose_name="密钥")
    url = models.CharField(max_length=255, null=True, blank=True, db_comment="自定义 API 地址", verbose_name="自定义 API 地址")
    status = models.SmallIntegerField(
        choices=CommonStatus.choices,
        default=CommonStatus.DISABLED,
        verbose_name="状态",
        db_comment="状态",
    )

    class Meta:
        db_table = "ai_api_key"
        verbose_name = "AI API 密钥"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AIModel(CoreModel):
    """ AI 模型 """
    name = models.CharField(max_length=64, db_comment="模型名字", verbose_name="模型名字")
    sort = models.IntegerField(db_comment="排序", default=0, verbose_name="排序")
    status = models.SmallIntegerField(
        choices=CommonStatus.choices,
        default=CommonStatus.DISABLED,
        verbose_name="状态",
        db_comment="状态",
    )
    key = models.ForeignKey(
        'AIApiKey',
        on_delete=models.CASCADE,
        db_comment='API 秘钥编号', verbose_name="API 秘钥编号"
    )
    platform = models.CharField(max_length=32, db_comment="模型平台", verbose_name="模型平台")
    model = models.CharField(max_length=64, db_comment="模型标识", verbose_name="模型标识")

    temperature = models.FloatField(null=True, blank=True, db_comment="温度参数", verbose_name="温度参数")
    max_tokens = models.IntegerField(null=True, blank=True, db_comment="单条回复的最大 Token 数量", verbose_name="单条回复的最大 Token 数量")
    max_contexts = models.IntegerField(null=True, blank=True, db_comment="上下文的最大 Message 数量", verbose_name="上下文的最大 Message 数量")

    class Meta:
        db_table = "ai_model"
        verbose_name = "模型配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
