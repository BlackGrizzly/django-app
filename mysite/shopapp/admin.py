from typing import Any
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from .admin_mixins import ExportToCSVMixin

from .models import Product, Order, ProductImage
from .forms import CSVImportForm
from .common import save_csv_products, save_csv_orders

class OrderInline(admin.TabularInline):
    model = Product.orders.through

class ProductImagesInline(admin.StackedInline):
    model = ProductImage

@admin.action(description="Опубликовать товар")
def mark_active(modeladmin: admin.ModelAdmin,  request: HttpRequest, queryset: QuerySet):
    queryset.update(active=True)

@admin.action(description="Снять товар с публикации")
def mark_deactive(modeladmin: admin.ModelAdmin,  request: HttpRequest, queryset: QuerySet):
    queryset.update(active=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportToCSVMixin):
    change_list_template = "admin/products_changelist.html"
    actions = [
        mark_active,
        mark_deactive,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductImagesInline,
    ]
    list_display = "pk", "name", "description_short", "price", "active"
    list_display_links = "pk", "name"
    ordering = "name",
    search_fields = "name", "description", "price"
    fieldsets = [
        (None, {
            "fields": ("name","description")
        }),
        ("Параметры товара", {
            "fields": ("price", "weight")
        }),
        ("Превью", {
            "fields": ("preview", ),
        }),
        ("Параметры отображения", {
            "fields": ("active", ),
            "classes": ("collapse", )
        }),
    ]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding
        )

        self.message_user(request, "Data from CSV was imported")
        return redirect("..")
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("import-products-csv/", self.import_csv, name="import_products_csv")]
        return new_urls + urls

class ProductInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportToCSVMixin):
    change_list_template = "admin/orders_changelist.html"
    list_display = "pk", "order_date", "delivery_address", "promocode", "comment", "user_verbose"
    list_display_links = "pk", "order_date"
    inlines = [
        ProductInline, 
    ]
    actions = [
        "export_csv",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Order.objects.select_related("user").prefetch_related("products")
    
    def user_verbose(self, obj: Order) -> str:
        return obj.user.username or obj.user.first_name
    
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        save_csv_orders(
            file=form.files["csv_file"].file,
            encoding=request.encoding
        )

        self.message_user(request, "Data from CSV was imported")
        return redirect("..")
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("import-orders-csv/", self.import_csv, name="import_orders_csv")]
        return new_urls + urls