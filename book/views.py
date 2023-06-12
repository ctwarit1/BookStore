from rest_framework import status, viewsets
from rest_framework.response import Response
from book.models import Book
from book.utils import RedisManager
from book.serializers import BookSerializer
from user.utils import authenticate_user, verify_superuser, verify_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from redis import Redis
from django.utils.decorators import method_decorator


"""
create ---> create data
lis  ---> all data
destroy ---> delete data by id
update ---> update data by id
retrieve ---> retrieve data by id
"""


# Create your views here.
class Books(viewsets.ViewSet):

    @swagger_auto_schema(request_body=BookSerializer)
    # @method_decorator(verify_superuser)
    @verify_superuser
    def create(self, request):
        """Create a Book"""

        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisManager().save(user_id=request.data.get("user"), book=serializer.data)
            return Response({"message": "Book Added Successful", "status": 201,
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def list(self, request):
        """Get all Books"""
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({"message": "All Books Fetched", "status": 202,
                             "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def retrieve(self, request, pk):
        """Retrieve a Book by id"""
        try:
            books = Book.objects.get(pk=pk)
            serializer = BookSerializer(books)
            return Response({"message": "Book with id fetched", "status": 200,
                             "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BookSerializer)
    @verify_superuser
    def update(self, request, pk):
        """Updating a Book"""
        try:
            books = Book.objects.get(pk=pk)
            serializer = BookSerializer(books, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book Updated", "status": 201,
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    def destroy(self, request, pk):
        """Deleting a Book"""
        try:
            books = Book.objects.get(pk=pk)
            books.delete()
            return Response({"message": "Book Deleted", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
