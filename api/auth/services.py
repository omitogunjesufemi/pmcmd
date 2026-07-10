from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ParseError
from api.auth.models import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, email, password, first_name, last_name, role, department):
        if self.repo.user_exists(email) is True:
            raise ParseError(f"This email ({email}) already exists")

        user_data = {
            "email": email,
            "password": make_password(password),
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "department": department
        }
        return self.repo.create(**user_data)