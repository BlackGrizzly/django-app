"""
Модуль api представлений.

В данном модуле описаны api представления интернет-магазина
"""

from django.http import HttpResponse, HttpRequest
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from csv import DictWriter
from .common import save_csv_products

@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    '''
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = "name", "description", "active", "price"
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = "name", "description"
    ordering_fields = "active", "name", "price"

    @extend_schema(
            summary="Get one Product by ID",
            description="Retrieve Product, return 404 if not found",
            responses={
                200: ProductSerializer,
                404: OpenApiResponse(description="Empty response, Product by id not found"),
            }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        file_name = "products_export.csv"
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = ["name", "description", "price"]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field) 
                for field in fields
            })

        return response
    
    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    '''
    Набор представлений для действий над Order
    Полный CRUD для сущностей заказа
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = "order_date", "delivery_address", "user", "products"
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = "comment", "delivery_address"
    ordering_fields = "pk", "order_date"