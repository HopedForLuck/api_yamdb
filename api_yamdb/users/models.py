from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

LENGTH_EMAIL = 254
LENGTH_USERNAME = 150
LENGTH_ROLE = 16
LENGTH_CODE = 36


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
        max_length=LENGTH_USERNAME,
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
        max_length=LENGTH_EMAIL,
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
        max_length=LENGTH_ROLE,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )
    confirmation_code = models.CharField(
        max_length=LENGTH_CODE,
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
