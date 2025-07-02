from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from system.models import User, Menu, LoginLog

from utils.serializers import CustomModelSerializer
from utils.custom_model_viewSet import CustomModelViewSet


class UserSerializer(CustomModelSerializer):
    roles = serializers.SerializerMethodField()  # 新增字段
    """
    用户数据 序列化器
    """
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'create_time', 'update_time']

    def get_roles(self, obj):
        """
        返回用户所有角色的名称列表
        """
        return list(obj.role.values_list('name', flat=True))

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # 更新登录IP和登录时间
        user.login_ip = request.META.get('REMOTE_ADDR')
        user.last_login = timezone.now()
        user.save(update_fields=['login_ip', 'last_login'])
        user_data = UserSerializer(user).data
        # 记录登录日志
        LoginLog.objects.create(
            username=user.username,
            result=LoginLog.LoginResult.SUCCESS,
            user_ip=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        # 在序列化后的数据中加入 accessToken
        user_data['accessToken'] = token.key
        return Response({
            "code": 0,
            "data": user_data,
            "error": None,
            "message": "ok"
        })


class UserInfo(APIView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserSerializer(user).data
        if user.is_superuser:
            roles = ['admin']
            # menus = Menu.objects.filter(pid__isnull=True).order_by('sort')
            permissions = Menu.objects.filter(type='button').order_by('auth_code').values_list('auth_code', flat=True)
        else:
            roles = user.get_role_name
            # menus = Menu.objects.filter(pid__isnull=True, role__users=user).order_by('sort').distinct()
            permissions = Menu.objects.filter(type='button', role__users=user).order_by('auth_code').distinct().values_list('auth_code', flat=True)
        # menus_data = MenuSerializer(menus, many=True).data
        user_data['roles'] = roles
        user_data['permissions'] = permissions
        return Response({
            "code": 0,
            "data": user_data,
            "error": None,
            "message": "ok"
        })


class Codes(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            "code": 0,
            "data": [
                "AC_100100",
                "AC_100110",
                "AC_100120",
                "AC_100010"
            ],
            "error": None,
            "message": "ok"
        })


class UserViewSet(CustomModelViewSet):
    """
    用户数据 视图集
    """
    queryset = User.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = UserSerializer
    read_only_fields = ['id', 'create_time', 'update_time', 'login_ip']
    filterset_fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'remark', 'creator',
                        'modifier', 'is_deleted', 'mobile', 'nickname', 'gender', 'language', 'city', 'province',
                        'country', 'avatar_url', 'status']
    search_fields = ['name']  # 根据实际字段调整
    ordering_fields = ['create_time', 'id']
    ordering = ['-create_time']


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # user = request.user
        # 删除用户的Token
        # Token.objects.filter(user=user).delete()
        return Response({
            "code": 0,
            "data": None,
            "error": None,
            "message": "登出成功"
        })

