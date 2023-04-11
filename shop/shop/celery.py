import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
app = Celery("shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'retrieve_book_data_from_api': {
        'task': 'shop_app.tasks.retrieve_book_data_from_api',
        'schedule': 30.0,
    },
}
