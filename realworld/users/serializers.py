from rest_framework import serializers
from users.models import User

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