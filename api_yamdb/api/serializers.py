from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для GET запросов."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleNotSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для небезопасных запросов."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    # def validate(self, data):
    #     request = self.context['request']
    #     author = request.user
    #     title_id = self.context.get('title_id')

    #     # title_id = self.context.get('view').self.kwargs.get('title_id')
    #     # title = get_object_or_404(Title, pk=title_id)
    #     if (
    #             self.request.method == 'POST'
    #             and Review.objects.filter(title=title_id, author=author).exists()
    #     ):
    #         raise serializers.ValidationError(
    #             'Может существовать только один отзыв!'
    #         )
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
