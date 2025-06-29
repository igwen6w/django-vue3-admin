from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    """
    使用 'Bearer' 前缀的 Token 认证
    """
    keyword = 'Bearer'