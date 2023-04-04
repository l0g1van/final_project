from rest_framework import serializers

from .models import Book, Order, OrderItem


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

