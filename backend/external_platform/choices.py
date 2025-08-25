from django.db import models

class PlatformAuthStatus(models.TextChoices):
    ACTIVE = 'active', '活跃'
    EXPIRED = 'expired', '过期'
    FAILED = 'failed', '失败'

class ApiMethod(models.TextChoices):
    GET = 'GET', 'GET'
    POST = 'POST', 'POST'
    PUT = 'PUT', 'PUT'
    DELETE = 'DELETE', 'DELETE'