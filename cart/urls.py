from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import ItemsCart

# creating router object
router = DefaultRouter()

# register Books view wit router
router.register('carts', ItemsCart, basename='cart')

urlpatterns = [
    path('', include(router.urls))

]