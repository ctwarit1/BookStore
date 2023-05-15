from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import UserSerializers, UserLoginSerializers
from user.utils import encode


# Create your views here.
def first_func(request):
    return Response({"message": "Hello World"})


class UserReg(APIView):

    def post(self, request):
        try:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "User registration Successful", "status": 201,
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class UserLog(APIView):

    def post(self, request):
        try:
            serializer = UserLoginSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = encode({"user": serializer.data.get("id")})
            return Response({"message": "User Logged In ", "status": 202, "data": token},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
