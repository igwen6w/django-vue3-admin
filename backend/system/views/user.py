from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from system.models import User
from utils.custom_model_viewSet import CustomModelViewSet


class UserSerializer(CustomModelViewSet):
    class Meta:
        model = User
        exclude = ('password',)


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "code": 0,
            "data": {
                "id": user.id,
                "password": user.password,
                "realName": user.nickname,
                "roles": [
                    "super"
                ],
                "username": user.username,
                "accessToken": token.key
            },
            "error": None,
            "message": "ok"
        })


class UserInfo(APIView):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        return Response({
            "code": 0,
            "data": {
                "id": user.id,
                "realName": user.username,
                "roles": [
                    "super"
                ],
                "username": user.username,
            },
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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer