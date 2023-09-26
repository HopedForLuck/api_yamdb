from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title
from .mixins import CreateListDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer, TitleNotSafeSerializer, TitleSafeSerializer


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
    pass


class CommentViewSet(ModelViewSet):
    pass