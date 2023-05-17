import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from user.models import User


def encode(payload):
    if "exp" not in payload.keys():
        payload.update(exp=datetime.utcnow() + timedelta(hours=1))
    return jwt.encode(payload, settings.SECRET, algorithm=settings.ALGORITHMS)


def decode(token):
    try:
        return jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHMS])
    except jwt.PyJWTError as ex:
        raise Exception(ex)


def authenticate_user(request):
    token = request.headers.get("token")
    if not token:
        raise Exception("Token not found")
    decoded = decode(token)
    if not decoded:
        raise Exception("Token Authentication required")
    user = User.objects.get(id=decoded.get("user"))
    if not user:
        raise Exception("Invalid User")
    request.data.update({"user": user.id})

    return user


def verify_user(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            user = authenticate_user(request)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return function(self, request, *args, **kwargs)

    return wrapper


def verify_superuser(function):
    def wrapper(self, request, *args, **kwargs):
        user = authenticate_user(request)

        if not user.is_superuser:
            return Response({"message": "User is not Authorized"}, status=status.HTTP_400_BAD_REQUEST)

        return function(self, request, *args, **kwargs)

    return wrapper
