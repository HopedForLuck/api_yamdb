import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_ADMIN
from users.models import LENGTH_USERNAME, LENGTH_EMAIL

User = get_user_model()


class MetaMixin(serializers.ModelSerializer):

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=LENGTH_USERNAME,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = serializers.EmailField(required=True, max_length=LENGTH_EMAIL)

    class Meta:
        model = User
        fields = ("username", "email")

    def send_email(self, email, code):
        send_mail(
            "Регистрация",
            f"Ваш код подтверждения! - {code}",
            EMAIL_ADMIN,
            [email],
            fail_silently=True,
        )

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError(
                'Запрещено имя "me", придумайте другое имя!'
            )
        return username

    def create(self, validated_data):

        username = validated_data['username']
        email = validated_data['email']
        code = uuid.uuid4()

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise ValidationError("У данного пользователя другая почта!")
            # validated_data['confirmation_code'] = code
            user.confirmation_code = code
            user.save()
            self.send_email(email=email, code=code)
            return validated_data
        else:
            if User.objects.filter(email=email).exists():
                raise ValidationError("Этот адрес уже занят!")
            validated_data['confirmation_code'] = code
            self.send_email(email=email, code=code)

            return User.objects.create(**validated_data)


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField(
            required=False
        )
        self.fields["password"] = serializers.HiddenField(default="")

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs["username"])
        if self.user.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("Неверный код подтверждения")
        data = str(self.get_token(self.user))

        return {"token": data}


class UserSerializer(MetaMixin):
    pass


class MeSerializer(MetaMixin):

    class Meta(MetaMixin.Meta):
        read_only_fields = ("role",)
