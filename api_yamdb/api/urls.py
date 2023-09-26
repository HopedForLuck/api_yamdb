from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,)

from .views import TitleViewSet, GenreViewSet, CommentViewSet, ReviewViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews")
router.register(
    r"reviews/(?P<review_id>\d+)/comments/(?P<id>\d+)",
    CommentViewSet,
    basename="comments")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('auth/signup/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/jwt/refresh/',
    #      TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/',
         TokenVerifyView.as_view(), name='token_verify'),
]