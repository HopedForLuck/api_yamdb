from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class MetaMixin(serializers.ModelSerializer):

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )
        model = User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError(
                'Запрещено имя "me", придумайте другое имя!'
            )
        return username


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
