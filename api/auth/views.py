from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer, \
    TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from api.auth.serializers import RegisterUserSerializer, UserSerializer, CustomTokenBlacklistSerializer
from api.auth.services import UserService
from api.core.views.base import BaseCreateAPIView


@extend_schema(
    tags=['Authentication'],
    request=RegisterUserSerializer,
    responses=UserSerializer
)
class RegisterUserView(BaseCreateAPIView):
    service_class = UserService
    create_service_method = "create_user"
    input_serializer_class = RegisterUserSerializer
    output_serializer_class = UserSerializer
    resource_name = "User"


@extend_schema(
    tags=['Authentication'],
    request=TokenObtainPairSerializer,
    responses=TokenObtainPairSerializer
)
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Lax',
            )
        return response


@extend_schema(
    tags=['Authentication'],
    request=TokenRefreshSerializer,
    responses=TokenRefreshSerializer
)
class PMTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token not found in cookie.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['refresh'] = refresh_token
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=serializer.validated_data['access'],
            httponly=True,
            samesite='Lax',
        )

        if 'refresh' in serializer.validated_data:
            response.set_cookie(
                key='refresh_token',
                value=serializer.validated_data['refresh'],
                httponly=True,
                samesite='Lax',
            )
        return response


@extend_schema(
    tags=['Authentication'],
    request=CustomTokenBlacklistSerializer,
    responses=CustomTokenBlacklistSerializer
)
class LogOutView(TokenBlacklistView):
    serializer_class = CustomTokenBlacklistSerializer

    def post(self, request: Request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token not found in cookie.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['refresh'] = refresh_token
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response
