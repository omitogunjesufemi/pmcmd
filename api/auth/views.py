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


@extend_schema(
    tags=['Authentication'],
    request=TokenRefreshSerializer,
    responses=TokenRefreshSerializer
)
class PMTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

@extend_schema(
    tags=['Authentication'],
    request=CustomTokenBlacklistSerializer,
    responses=CustomTokenBlacklistSerializer
)
class LogOutView(TokenBlacklistView):
    serializer_class = CustomTokenBlacklistSerializer
