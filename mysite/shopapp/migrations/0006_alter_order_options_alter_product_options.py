# Generated by Django 4.2.1 on 2023-08-03 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['order_date']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
    ]
