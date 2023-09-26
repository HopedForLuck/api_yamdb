from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # user, admin, moderator
    role = models.CharField('Роль пользователя', max_length=9)
    bio = models.TextField('Биография', max_length=256, blank=True, null=True)
