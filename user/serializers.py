from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User
from user.utils import encode


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'phone', 'is_superuser',
                  'is_verified']
        extra_kwargs = {'password': {'write_only': True}, "is_verified": {'required': False, 'allow_null': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])

        if not user:
            raise Exception("Invalid Credentials")
        if not user.is_verified:
            raise Exception("User Not Verified")
        token = encode({"user": user.id})
        self.context.update({"token": token})
        return user
