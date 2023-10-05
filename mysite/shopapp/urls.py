from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView,
    ProductDetailView, 
    ProductCreateView, 
    ProductUpdateView, 
    ProductDeleteView,  
    ShopIndexView, 
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ExportOrdersView,
    LatestProductsFeed,
    UserOrdersListView,
    ExportUserOrdersView,
)
from .api import ProductViewSet, OrderViewSet

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/edit", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/deactivate", ProductDeleteView.as_view(), name="product_deactivate"),
    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/edit", OrderUpdateView.as_view(), name="order_edit"),
    path("orders/<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/export/", ExportOrdersView.as_view(), name="export_orders"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("users/<int:user_id>/orders/export/", ExportUserOrdersView.as_view(), name="export_user_orders"),
]