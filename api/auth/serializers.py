from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from api.auth.models import User
from utils.constants import Roles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'email', 'role', 'department'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get('email')
        data = super().validate(attrs)
        return data


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    role = serializers.ChoiceField(choices=Roles.choices, required=True)
    department = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(required=True)


class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            'success': True,
            'message': 'You have successfully logged out.',
        })
        return data