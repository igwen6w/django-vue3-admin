import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from rest_framework.exceptions import ValidationError
from django.utils import timezone

def validate_mobile(value):
    if value and not re.findall(r"1\d{10}", value):
        raise ValidationError('手机格式不正确')


def validate_amount(value):
    if value is None:
        raise ValidationError('金额不能为空')
    if value and value < 0:
        raise ValidationError('金额不能为负')


def to_cent(value):
    if value is None:
        value = 0
    return Decimal(value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

# 定义一个小工具：从时间戳转换为 aware datetime（如果时间戳有效）
def ts_to_aware(ts):
    if ts:
        naive_dt = datetime.fromtimestamp(ts)
        return timezone.make_aware(naive_dt)
    return None