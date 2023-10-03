from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь")
    ]
    REQUIRED_FIELDS = ["email", "password"]

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        blank=True,
        unique=True,
        error_messages={
            'unique': "Пользователь с такой почтой уже существует",
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

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ("id",)
        unique_together = (("username", "email"),)
