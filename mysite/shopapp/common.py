"""
Модуль общих функций.

В данном модуле описаны общие функции
"""
from io import TextIOWrapper
from csv import DictReader
from .models import Product, Order
from django.contrib.auth.models import User
from typing import Sequence
import re

def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]

    Product.objects.bulk_create(products)
    return products

def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)
    orders = []
    #{'id': '1', 
    # 'order_date': '2023-06-27 20:46:13.872013+00:00', 
    # 'comment': '', 
    # 'delivery_address': 'ул. Строителей, д.5', 
    # 'promocode': 'NEW2023', 
    # 'user': 'admin', 
    # 'products': '2, 1, 3'}
    for row in reader:
        user = User.objects.get(username=row['user'])
        products_ids = row['products'].split(',')
        products: Sequence[Product] = Product.objects.filter(id__in=products_ids)
        order, created = Order.objects.get_or_create(
            id=row['id'],
            order_date=row['order_date'],
            comment=row['comment'],
            delivery_address=row['delivery_address'],
            promocode=row['promocode'],
            user=user,
        )
        if created:
            for product in products:
                order.products.add(product)
            order.save()
            orders.append(order)
    return orders