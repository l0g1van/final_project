# Generated by Django 4.1.7 on 2023-04-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0003_alter_book_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_work', 'in_work'), ('success', 'success'), ('fail', 'fail')], default='in_work', max_length=20),
        ),
    ]
