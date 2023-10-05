from typing import Any, Optional
from django.core.management import BaseCommand
from shopapp.models import Order, Product

class Command(BaseCommand):
    '''Связь заказа и товара'''
    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Создание связи заказа и товаров")
        order = Order.objects.first()
        if not order:
            self.stdout.write(f"Заказов не найдено")
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(self.style.SUCCESS(f"Товары {order.products.all()} добавлены в заказ {order}"))