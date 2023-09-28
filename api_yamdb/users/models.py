from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    ROLE_CHOISES = [
        ("user", "Аутентифицированный пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    ]
    role = models.TextField('Роль', choices=ROLE_CHOISES)
    bio = models.TextField('Биография', blank=True)
