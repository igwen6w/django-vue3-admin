# -*- coding: utf-8 -*-

"""
@Remark: 公共基础model类
"""
from django.db import models

class CoreModel(models.Model):
    remark = models.CharField(max_length=256, verbose_name="备注", null=True, blank=True, help_text="备注")
    creator = models.CharField(max_length=64, null=True, blank=True, help_text="创建人", verbose_name="创建人")
    modifier = models.CharField(max_length=64, null=True, blank=True, help_text="修改人", verbose_name="修改人")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")
    is_deleted = models.BooleanField(default=False, verbose_name='是否软删除')

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
