from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Book, Order


# class HomePageView(generic.ListView):
#     model = Book
#     template_name = 'home_page.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


@login_required(login_url='/login/')
def profile_view(request, pk):
    profile = User.objects.get(id=pk)
    return render(request, 'profile.html', {'profile': profile})


def logout_view(request):
    logout(request)
    return redirect('home')


def home_page(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'home_page.html', context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user_id=customer, status='in_work')
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context=context)


def checkout(request):
    context = {}
    return render(request, 'checkout.html')
