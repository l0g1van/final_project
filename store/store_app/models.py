from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=230)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default='No_image_available.svg.png')
    quantity = models.IntegerField(default=0)

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    # user_email = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ('in_work', 'in_work'),
        ('success', 'success'),
        ('fail', 'fail')
    ), default='in_work')
    # delivery_address = models.CharField(max_length=250)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_store_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class DeliveryAddress(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    country = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.address
