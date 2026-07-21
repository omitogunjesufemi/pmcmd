from typing import Optional

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
