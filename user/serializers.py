from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'phone']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise Exception("Invalid Credentials")
        return user

