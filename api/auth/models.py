from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        PM = "pm", "Project Manager"
        PMO_HEAD = "pmo_head", "Head, Project Management"

    role = models.CharField(
        choices=Roles.choices,
        default=Roles.PM,
        max_length=40,
    )
    department = models.CharField(
        max_length=30,
        blank=True
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        ordering = ['first_name', 'last_name']