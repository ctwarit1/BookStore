from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import ItemsCart, OrderAPI

# creating router object
router = DefaultRouter()

# register Books view wit router
router.register('carts', ItemsCart, basename='cart')
router.register('order', OrderAPI, basename='order')

urlpatterns = [
    path('', include(router.urls))

]
