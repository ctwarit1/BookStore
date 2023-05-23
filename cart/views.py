from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from cart.serializers import CartSerializers
from user.utils import verify_user
from cart.models import Cart


# Create your views here.
class ItemsCart(viewsets.ViewSet):

    @verify_user
    def create(self, request):
        """Creating a Cart"""
        try:
            serializer = CartSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Cart is Added", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def list(self, request):
        """Get Cart"""
        try:
            carts = Cart.objects.filter(user_id=request.data.get("user"))
            serializer = CartSerializers(carts, many=True)
            return Response({"message": "Cart Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def destroy(self, request, pk):
        """Deleting a Cart"""
        try:
            carts = Cart.objects.get(pk=pk, user_id=request.data.get("user"))
            carts.delete()
            return Response({"message": "Cart Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class OrderAPI(viewsets.ViewSet):
    @verify_user
    def create(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get("cart"), user_id=request.data.get("user"))
            print(cart)
            cart.status = True
            cart.save()

            return Response({"message": "Active Cart", "status": 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def list(self, request):
        try:
            cart = Cart.objects.filter(user_id=request.data.get("user"), status=True)
            serializer = CartSerializers(cart, many=True)

            return Response({"message": "Active Cart Fetched", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def destroy(self, request, pk):
        try:
            cart = Cart.objects.get(user_id=request.data.get("user"), pk=pk, status=True)
            cart.delete()

            return Response({"message": "Active Cart Deleted", "status": 201, "data": {}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)