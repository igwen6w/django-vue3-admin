from django.db import models

from utils.models import CoreModel
from utils.utils import validate_mobile


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

