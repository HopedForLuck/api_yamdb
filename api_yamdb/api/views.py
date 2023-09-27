from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comment, Genre, Review, Title

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
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleNotSafeSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsSuperUserIsAdminIsModeratorIsAuthor,
    # )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsSuperUserIsAdminIsModeratorIsAuthor,
    # )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
