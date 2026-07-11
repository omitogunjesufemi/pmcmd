from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import NotFound
from api.auth.models import UserRepository
from utils.exceptions import ServiceException


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, email, password, first_name, last_name, role, department):
        if self.repo.user_exists(email) is True:
            raise ServiceException(f"This email ({email}) already exists")

        user_data = {
            "email": email,
            "password": make_password(password),
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "department": department
        }
        return self.repo.create(**user_data)

    def get_by_id(self, user_id):
        user = self.repo.get_by_id(id=user_id)
        if not user:
            raise NotFound(f"User with ID: {user_id} not found.")
        return user