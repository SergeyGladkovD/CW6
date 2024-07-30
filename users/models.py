from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": "True", "null": "True"}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    avatar = models.ImageField(
        upload_to="media/avatar/", verbose_name="аватар", **NULLABLE
    )
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="страна", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [
            ("can_block_users", "Can block users"),
            ("view_all_users", "Can view all users"),
        ]
