from django.contrib import admin
from.models import Book, Order, OrderItem, DeliveryAddress
# Register your models here.
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)

