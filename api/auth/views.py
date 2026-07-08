from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import RegisterUserSerializer, UserSerializer
from api.auth.services import UserService
from api.core.views.base import BaseCreateAPIView


@extend_schema(
    request = RegisterUserSerializer,
    responses = UserSerializer
)
class RegisterUserView(BaseCreateAPIView):
    service_class = UserService
    create_service_method = "create_user"
    input_serializer_class = RegisterUserSerializer
    output_serializer_class = UserSerializer
    resource_name = "User"


@extend_schema(
    request=TokenObtainPairSerializer,
    responses=TokenObtainPairSerializer
)
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class LogOutView:
    pass