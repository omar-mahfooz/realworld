from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import pdb
from rest_framework.exceptions import AuthenticationFailed


class RegistrationResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    bio = serializers.CharField(default='')
    image = serializers.CharField(default='')
    token = serializers.CharField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = ({'password': {'write_only':True}})
    
    def create(self, validated_data):
        """Creates User with validated data"""
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = ({'password': {'write_only':True}})
    

# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed

# User = get_user_model()

# class UserAuthenticationSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Both email and password are required fields.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            # If authentication is successful, generate a JWT token
            refresh = RefreshToken.for_user(user)
            data['user'] = user
            data['token'] = str(refresh.access_token)
            return data
        else:
            raise AuthenticationFailed('Invalid credentials.')