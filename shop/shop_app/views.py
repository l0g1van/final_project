import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Book, Order, OrderItem, DeliveryAddress


# class HomePageView(generic.ListView):
#     model = Book
#     template_name = 'home_page.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


# @login_required(login_url='/login/')
# def profile_view(request, pk):
#     profile = User.objects.get(id=pk)
#     return render(request, 'profile.html', {'profile': profile})


def logout_view(request):
    logout(request)
    return redirect('home')


# @login_required(login_url='/login/')
def home_page(request):
    # price = request.GET.get('price')
    books = Book.objects.all()

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
    context = {'cart_items': cart_items, 'books': books}

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

    for order_item in order.orderitem_set.all():
        if order.status == 'ordered':
            book = order_item.book_id
            book.quantity -= order_item.quantity
            book.save()

    DeliveryAddress.objects.create(
        user_id=customer,
        order_id=order,
        address=data['delivery']['address'],
        city=data['delivery']['city'],
        country=data['delivery']['country']
    )
    return JsonResponse('Item was added', safe=False)
