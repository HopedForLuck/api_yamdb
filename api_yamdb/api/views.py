from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comment, Genre, Review, Title

from .mixins import CreateListDestroyViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleNotSafeSerializer, TitleSafeSerializer,
                          ReviewSerializer, CommentSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleNotSafeSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthorOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
