import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets, mixins, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsSuperUserOrIsAdminOnly
from .serializers import (SignUpSerializer, TokenSerializer,
                          UserSerializer, MeSerializer)

User = get_user_model()


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def send_email(self, email, code):
        send_mail(
            "Регистрация",
            f"Ваш код подтверждения! - {code}",
            "from@example.com",
            [email],
            fail_silently=True,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data.get("username")
        email = serializer.initial_data.get("email")
        code = uuid.uuid4()
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise ValidationError("У данного пользователя другая почта!")
            serializer.is_valid(raise_exception=False)
            user.confirmation_code = uuid.uuid4()
            user.save()
        else:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.confirmation_code = uuid.uuid4()
            user.set_unusable_password()
            user = serializer.save()
        self.send_email(
            email=email,
            code=code
        )
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
