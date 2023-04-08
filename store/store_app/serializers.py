from rest_framework import serializers

from .models import Book, Order, OrderItem


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        # fields = '__all__'
        fields = ['title', 'price']


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['user_email', 'delivery_address', 'status']
