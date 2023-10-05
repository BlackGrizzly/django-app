from typing import Any, Optional, Sequence
from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    '''Создание заказа'''
    @transaction.atomic
    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Создание заказа")
        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.all()
        order, created = Order.objects.get_or_create(
            delivery_address="ул. Строителей, д.5",
            promocode="NEW2023",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        if created:
            self.stdout.write(f"Заказ {order} создан")
        self.stdout.write(self.style.SUCCESS("Заказы созданы"))