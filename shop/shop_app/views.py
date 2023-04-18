import json

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Book, Order, OrderItem, DeliveryAddress
from .tasks import send_mail_order_created


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return redirect('home')


def home_page(request):
    # price = request.GET.get('price')
    # books = Book.objects.all()
    min_max_price = Book.objects.aggregate(Min('price'), Max('price'))

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user_id=customer, status='in_work')
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    # if price:
    #     price_range = price.split('-')
    #     min_price = price_range[0]
    #     max_price = price_range[1]
    #     books = books.filter(price__gte=min_price, price__lte=max_price)

    max_price = request.GET.get('max_price')
    if max_price:
        books = Book.objects.filter(price__lte=max_price)
    else:
        books = Book.objects.all()
    context = {'cart_items': cart_items, 'books': books, 'min_max_price': min_max_price}

    return render(request, 'home_page.html', context=context)


@login_required(login_url='/login/')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user_id=customer, status='in_work')
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'cart.html', context=context)


@login_required(login_url='/login/')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user_id=customer, status='in_work')
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'checkout.html', context=context)


@login_required(login_url='/login/')
def updateItem(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']

    customer = request.user
    book = Book.objects.get(id=bookId)

    order, created = Order.objects.get_or_create(user_id=customer, status='in_work')

    orderItem, created = OrderItem.objects.get_or_create(order_id=order, book_id=book)

    if action == 'add':
        # orderItem.quantity = (orderItem.quantity + 1)
        if book.quantity > orderItem.quantity:
            orderItem.quantity += 1
        else:
            return JsonResponse({'error': 'Insufficient quantity.'}, status=400)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    if orderItem.quantity > 0:
        orderItem.save()

    else:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='/login/')
def process_order(request):
    data = json.loads(request.body)
    customer = request.user
    order, created = Order.objects.get_or_create(user_id=customer, status='in_work')
    order.status = 'ordered'
    order.save()
    books = {}
    for order_item in order.orderitem_set.all():
        if order.status == 'ordered':
            book = order_item.book_id
            book.quantity -= order_item.quantity
            book.save()
            data_for_api_order_item = {
                'order_id': order.pk,
                'book_store_id': book.title,
                'quantity': order_item.quantity
            }
            books[f'{book.title}'] = order_item.quantity
            data_for_api_book = {
                'book_title': book.title,
                'book_quantity': book.quantity
            }
            requests.patch(f'http://127.0.0.1:8001/books/{book.pk}/', data=data_for_api_book)
            requests.post('http://127.0.0.1:8001/order_item/', data=data_for_api_order_item)

    DeliveryAddress.objects.create(
        user_id=customer,
        order_id=order,
        address=data['delivery']['address'],
        city=data['delivery']['city'],
        country=data['delivery']['country']
    )
    data_for_api_delivery_address = {
        'order_id': order.pk,
        'address': data['delivery']['address'],
        'city': data['delivery']['city'],
        'country': data['delivery']['country']
    }
    send_mail_order_created(user_email=customer.email, user_order=order.pk, books=books)
    requests.post('http://127.0.0.1:8001/delivery_address/', data=data_for_api_delivery_address)
    return redirect('home')
