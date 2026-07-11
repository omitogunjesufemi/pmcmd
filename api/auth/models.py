import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from api.core.repositories.base import BaseRepository
from utils.constants import Roles


class CustomUserManager(UserManager):
    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        if email is None:
            email = username

        username = email.split('@')[0] if email else 'admin'
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        choices=Roles.choices,
        default=Roles.PM,
        max_length=40,
    )
    department = models.CharField(
        max_length=30,
        blank=True
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        ordering = ['first_name', 'last_name']


class UserRepository(BaseRepository):
    model = User
    def get_by_username(self, email):
        return self.model.objects.filter(email=email).first()

    def user_exists(self, email):
        return self.model.objects.filter(email=email).exists()