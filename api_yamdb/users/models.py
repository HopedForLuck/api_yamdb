# from djchoices import ChoiceItem, DjangoChoices
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES_CHOISES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
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
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=10,
        verbose_name='Роль',
        choices=ROLES_CHOISES,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
