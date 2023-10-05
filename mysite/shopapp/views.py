"""
Модуль представлений.

В данном модуле описаны представления интернет-магазина
"""
import logging
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from timeit import default_timer

from django.core import serializers
from django.core.cache import cache
from .forms import ProductForm
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _
from .models import Product, Order, ProductImage

log = logging.getLogger(__name__)

class ShopIndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('laptop', 'last model of laptop', 1999),
            ('desktop', 'super power pc', 2999),
            ('smartphone', 'overprice smartphone', 999),  
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Render shop index")
        return render(request, "shopapp/shop-index.html", context=context)
    
class ProductListView(ListView):
    queryset = Product.objects.filter(active=True)
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "description", "price", "weight"
    success_url = reverse_lazy("shopapp:product_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form) 

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    #fields = "name", "description", "price", "weight", "preview"
    form_class = ProductForm
    template_name_suffix = '_update_form'

    def test_func(self) -> bool | None:
        user = self.request.user
        product = self.get_object()
        return user.is_superuser or (user.has_perm("shopapp.change_product") and product.created_by == user)
    
    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response

    def get_success_url(self) -> str:
        return reverse("shopapp:product_detail", kwargs={"pk": self.object.pk})

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shopapp.delete_product"
    queryset = Product.objects.prefetch_related("images")
    success_url = reverse_lazy("shopapp:product_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10

class OrderDetailView(LoginRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    model = Order

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = "user", "products", "comment", "delivery_address", "promocode"
    success_url = reverse_lazy("shopapp:order_list")

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = "user", "products", "comment", "delivery_address", "promocode"
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse("shopapp:order_detail", kwargs={"pk": self.object.pk})
    
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")

class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_orders_list.html'

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
        return Order.objects.filter(user=self.owner)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context
    
class ExportOrdersView(UserPassesTestMixin, View):
    
    
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": [product.pk for product in order.products.order_by("pk").all()]
            }
            for order in orders 
        ]
        return JsonResponse({"orders": orders_data})
    
    def test_func(self) -> bool | None:
        user = self.request.user
        return user.is_staff
    
class ExportUserOrdersView(UserPassesTestMixin, View):
    
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user_id = kwargs["user_id"]
        cache_key = "orders_serialized_" + str(user_id)
        orders_serialized = cache.get(cache_key)
        if orders_serialized is None:
            owner = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(user=owner).order_by("pk")
            orders_serialized = serializers.serialize('json', orders)
            cache.set(cache_key, orders_serialized, 300)
        return JsonResponse(orders_serialized, safe=False)

    def test_func(self) -> bool | None:
        user = self.request.user
        return user.is_staff

class LatestProductsFeed(Feed):
    title = "Products Feed"
    description = "Adding and changing products"
    link = reverse_lazy("shopapp:product_list")

    def items(self):
        return (Product.objects.filter(active=True).order_by("-last_change_date")[:10])
    
    def item_title(self, item: Product) -> str:
        return item.name
    
    def item_description(self, item: Product) -> str:
        return item.description_short