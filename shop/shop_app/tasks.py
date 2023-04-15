from celery import shared_task
import requests
from io import BytesIO

from django.core.mail import send_mail

from .models import Book


@shared_task()
def retrieve_book_data_from_api():
    response = requests.get('http://127.0.0.1:8001/books/')
    # print(response.json())
    Book.objects.all().delete()
    for el in response.json():
        title = el['title']
        price = el['price']
        quantity = el['quantity']
        img_file = BytesIO(requests.get(el['image']).content)
        img_name = el['image'].split('/')[-1]
        # print(title, price, quantity, img_file, img_name)
        book = Book.objects.create(title=title, price=price, quantity=quantity)
        book.image.save(img_name, img_file, save=True)


@shared_task()
def send_mail_order_created(user_email, user_order, books):
    send_mail(
        'Your order created',
        f'Your order created with id {user_order} and contains: \n{books}',
        'server@noreply.com',
        [f'{user_email}'],
        fail_silently=False
    )
