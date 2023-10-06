from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.permissions import IsSuperUserOrIsAdminOnly
from .serializers import (MeSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer)

User = get_user_model()


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(request.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)


class MeProfileViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MeSerializer

    def retrieve(self, request, pk=None):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer
