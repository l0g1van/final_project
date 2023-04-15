from rest_framework import viewsets, permissions, response, status
from .serializers import OrderSerializer, BookSerializer, OrderItemSerializer, DeliveryAddressSerializer
from .models import Book, Order, OrderItem, DeliveryAddress
from .permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     book = Book.objects.get(title=request.data['book_title'])
    #     serializer = self.get_serializer(instance, data={
    #         'title': book.title,
    #         'price': book.price,
    #         'quantity': request.data['book_quantity'],
    #         'image': book.image
    #     }, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return response.Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        isinstance_ = self.get_object()
        book = Book.objects.get(title=request.data['book_title'])
        serializer = self.get_serializer(isinstance_, data={
            'title': book.title,
            'price': book.price,
            'image': book.image,
            'quantity': request.data['book_quantity']
        }, partial=False)
        serializer.is_valid()
        self.perform_update(serializer)
        return response.Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(pk=int(request.data["order_id"]), status='ordered')
        book = Book.objects.get(title=request.data['book_store_id'])
        serializer = self.get_serializer(data={
            'order_id': f'http://127.0.0.1:8001/order/{order.id}/',
            'book_store_id': f'http://127.0.0.1:8001/books/{book.id}/',
            'quantity':  int(request.data['quantity'])
        })
        if serializer.is_valid():
            self.perform_create(serializer)
            data = serializer.data
            return response.Response(data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer

    def create(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(pk=int(request.data["order_id"]), status='ordered')
        serializer = self.get_serializer(data={
            'order_id': f'http://127.0.0.1:8001/order/{order.id}/',
            'address': request.data['address'],
            'city': request.data['city'],
            'country': request.data['country']
        })
        if serializer.is_valid():
            self.perform_create(serializer)
            data = serializer.data
            return response.Response(data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
