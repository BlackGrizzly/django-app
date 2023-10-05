from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename
    )

class Product(models.Model):
    class Meta:
        ordering = ["name"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=False)
    weight = models.PositiveSmallIntegerField(default=0)
    last_change_date = models.DateTimeField(auto_now=True)
    add_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self) -> str:
        return f"Товар {self.name!r} (pk={self.pk})"
    
    def get_absolute_url(self):
        return reverse("shopapp:product_detail", kwargs={"pk": self.pk})
    
def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.pk,
        filename=filename
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(null=True, blank=True, upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order (models.Model):
    class Meta:
        ordering = ["order_date"]        
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    order_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")

    def __str__(self) -> str:
        return f"Заказ от пользователя {self.user!r} от {self.order_date}"
    
    def get_absolute_url(self):
        return reverse("shopapp:order_detail", kwargs={"pk": self.pk})