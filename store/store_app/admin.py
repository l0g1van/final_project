from django.contrib import admin

from .models import Book, Order, OrderItem, OrderItemBookItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    fieldsets = [
        ('Title', {'fields': ['title']}),
        ('Price', {'fields': ['price']})
    ]
    list_filter = ['price']
    search_fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'status']
    list_filter = ['status']


