from typing import Any, Optional
from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    '''Создание продукта'''
    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Создание продукта")
        products = [
            {"name": "Laptop", "price": 12000, },
            {"name": "Desktop", "price": 20000, },
            {"name": "Smartphone", "price": 10000, },
        ]
        for product in products:
            new_product, created = Product.objects.get_or_create(name=product["name"], price=product["price"])
            if created:
                self.stdout.write(f"Продукт {new_product.name} создан")
        self.stdout.write(self.style.SUCCESS("Продукты созданы"))