# Generated by Django 5.1.2 on 2024-10-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_order_receiving'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items_name',
            field=models.TextField(default='', verbose_name='Название продуктов заказе'),
        ),
    ]