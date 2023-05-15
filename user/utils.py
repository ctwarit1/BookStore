import jwt
from django.conf import settings
from datetime import datetime, timedelta


def encode(payload):
    if "exp" not in payload.keys():
        payload.update(exp=datetime.utcnow() + timedelta(hours=1))
    return jwt.encode(payload, settings.SECRET, algorithm=settings.ALGORITHMS)


def decode(token):
    try:
        return jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHMS])
    except jwt.PyJWTError as ex:
        raise Exception(ex)
