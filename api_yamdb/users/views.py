import uuid

from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import permissions, status, viewsets, mixins, filters

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
from api.permissions import IsSuperUserOrIsAdminOnly


User = get_user_model()


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError("Неверные данные")
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data["email"]
        code = uuid.uuid4()
        send_mail(
            "Регистрация",
            f"Ваш код подтверждения! - {code}",
            "from@example.com",
            [email],
            fail_silently=True,
        )
        instance.confirmation_code = code
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)


class MeProfileViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer
