from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь")
    ]
    REQUIRED_FIELDS = ["email", "password"]
    email = models.EmailField(
        ('email address'),
        blank=True,
        unique=True,
        error_messages={
            'unique': ("Пользователь с такой почтой уже существует"),
        },
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография",
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        verbose_name="Код потдверждения",
    )

    class Meta:
        ordering = ("id",)
        unique_together = (("username", "email"),)
