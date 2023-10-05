from .models import Product, Order
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "pk", "name", "description", "price", "weight", "add_date", "preview", "active"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "pk", "order_date", "comment", "delivery_address", "promocode", "products", "user"