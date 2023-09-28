from rest_framework.decorators import action
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .mixins import CreateListDestroyViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleNotSafeSerializer, TitleSafeSerializer,
                          ReviewSerializer, CommentSerializer)
from .permissions import (
    AnonimReadOnly,
    IsSuperUserIsAdminIsModeratorIsAuthor,
    IsSuperUserOrIsAdminOnly
)


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
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleNotSafeSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor,
    )

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor,
    )
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        comments = Review.objects.annotate(count=Count("comments"))
        return get_object_or_404(comments, pk=review_id,)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())
