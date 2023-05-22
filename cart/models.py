from django.db import models
from user.models import User
from book.models import Book


# Create your models here.
class Cart(models.Model):
    total_quantity = models.IntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    price = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
