from django.contrib.auth.models import AbstractUser
from django.db import models
from api.core.repositories.base import BaseRepository
from utils.constants import Roles


class User(AbstractUser):
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