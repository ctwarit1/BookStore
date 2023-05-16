from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import Books

# creating router object
router = DefaultRouter()
# register Books view wit router
router.register('books', Books, basename='book')

urlpatterns = [
    path('', include(router.urls))

]
