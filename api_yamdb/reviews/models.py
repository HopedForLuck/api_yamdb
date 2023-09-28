from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    """Класс категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс жанров."""

    name = models.CharField(
        max_length=75,
        unique=True,
        verbose_name='Hазвание',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=150,
        verbose_name='Hазвание',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[
            MinValueValidator(
                0,
                message='Это произведение слишком старо для нас'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Мы не можем заглядывать в будущее'
            )
        ],
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} относится к следующему(им) жанру(ам): {self.genre}'