# Generated by Django 4.1.7 on 2023-04-04 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=230)),
                ('price', models.DecimalField(decimal_places=2, max_digits=2)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.bookmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254)),
                ('delivery_address', models.CharField(max_length=250)),
                ('order_id_in_shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.ordermodel')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('book_store_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('order_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
    ]
