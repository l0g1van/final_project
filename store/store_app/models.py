from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=230)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class BookItem(models.Model):
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE)


class Order(models.Model):
    user_email = models.EmailField()
    status = models.CharField(max_length=20, choices=(
        ('in_work', 'in_work'),
        ('success', 'success'),
        ('fail', 'fail')
    ), default='in_work')
    delivery_address = models.CharField(max_length=250)


class OrderItem(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    book_store_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class OrderItemBookItem(models.Model):
    order_item_id = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    book_item_id = models.OneToOneField(BookItem, on_delete=models.CASCADE)
