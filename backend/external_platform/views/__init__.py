__all__ = [
    # API视图集将在需要时添加
    'RequestLogViewSet',
    'ExternalAuthCaptchaLogViewSet',
    'PlatformViewSet',
    'AuthSessionViewSet',
    'PlatformEndpointViewSet',
    'PlatformConfigViewSet'
]

from external_platform.views.request_log import RequestLogViewSet
from external_platform.views.external_auth_captcha_log import ExternalAuthCaptchaLogViewSet
from external_platform.views.platform import PlatformViewSet
from external_platform.views.auth_session import AuthSessionViewSet
from external_platform.views.platform_endpoint import PlatformEndpointViewSet
from external_platform.views.platform_config import PlatformConfigViewSet