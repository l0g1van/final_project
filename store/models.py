from django.db import models

from shop.models import OrderModel, BookModel


class Book(models.Model):
    title = models.CharField(max_length=230)
    price = models.DecimalField(max_digits=2, decimal_places=2)
    book = models.OneToOneField(BookModel, on_delete=models.CASCADE)


class Order(models.Model):
    user_email = models.EmailField()
    # status =
    delivery_address = models.CharField(max_length=250)
    order_id_in_shop = models.OneToOneField(OrderModel, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    book_store_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

