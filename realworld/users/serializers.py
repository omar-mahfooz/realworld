from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate




class RegistrationResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    bio = serializers.CharField(default="")
    image = serializers.CharField(default="")
    token = serializers.CharField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Creates User with validated data"""
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


User = get_user_model()


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data, request=None):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Both email and password are required fields."
            )

        user = authenticate(self.context["request"], username=email, password=password)

        if user is not None:
            # If authentication is successful, generate a JWT token
            refresh = RefreshToken.for_user(user)
            data["user"] = user
            data["token"] = str(refresh.access_token)
            return data
        else:
            raise AuthenticationFailed("Invalid credentials.")
