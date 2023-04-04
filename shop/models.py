from django.db import models
from django.contrib.auth.models import User


class BookModel(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=2, decimal_places=2)
    quantity = models.IntegerField()


class OrderModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # status =
    delivery_address = models.CharField(max_length=250)


class OrderItemModel(models.Model):
    order_id = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

