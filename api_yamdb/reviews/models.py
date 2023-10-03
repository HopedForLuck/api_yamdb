from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


def my_year_validator(value):
    if value < 0 or value > timezone.now().year:
        raise ValidationError(
            '%(value)s is not a correcrt year!',
            params={'value': value},
        )


def current_year():
    return timezone.now().year


class CommonClass(models.Model):
    """Вспомогательный класс с общими полями для моделей Genre и Category"""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг для категории содержит недопустимый символ'
        )]
    )


class Category(CommonClass):
    """Класс категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(CommonClass):
    """Класс жанров."""

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
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[my_year_validator],
        db_index=True
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
        return self.name[:10]


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
        return (
            f'{self.title} относится к следующему(им) жанру(ам): {self.genre}'
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Произведение",
    )
    text = models.TextField(
        max_length=200,
        verbose_name="Текст",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Нельзя поставить оценку ниже 1"),
            MaxValueValidator(10, "Нельзя поставить оценку больше 10")
        ],
        help_text="Оцените произведение по шкале от 1 до 10.",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Отзыв"
    )
    text = models.TextField(
        max_length=200,
        verbose_name="Текст"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.review[:10]
