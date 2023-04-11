from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Book, Order, OrderItem, DeliveryAddress


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        # fields = '__all__'
        fields = ['title', 'price', 'quantity', 'image']


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    # user_email = serializers.HyperlinkedRelatedField(
    #     view_name='user-detail',
    #     lookup_field='pk',
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['status']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    # order_id = serializers.RelatedField(many=True, read_only=True)
    # book_store_id = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order_id', 'book_store_id', 'quantity']


class DeliveryAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['order_id', 'address', 'city', 'country']

