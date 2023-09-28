from django.urls import include, path
from rest_framework import routers

# from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]
