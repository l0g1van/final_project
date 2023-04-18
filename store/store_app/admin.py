from django.contrib import admin

from .models import Book, Order, OrderItem, DeliveryAddress

admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    fieldsets = [
        ('Title', {'fields': ['title']}),
        ('Price', {'fields': ['price']}),
        ('Quantity', {'fields': ['quantity']}),
        ('Image', {'fields': ['image']})
    ]
    list_filter = ['price']
    search_fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status']
    list_filter = ['status']


