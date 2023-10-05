from django.test import TestCase
from django.urls import reverse
from random import choices
from string import ascii_letters
from .models import Product, Order
from django.contrib.auth.models import User, Permission

class ProductCreateViewTestCase(TestCase):

    fixtures = [
        "permission-fixture.json",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="test", password="qwerty")
        permission = Permission.objects.get(codename="add_product")
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        self.client.force_login(self.user)

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name, 
                "description": "Looper test", 
                "price": "122.34", 
                "weight": "2"
            }
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())

class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="test", password="qwerty")
        cls.product_name = "".join(choices(ascii_letters, k=10))
        cls.product = Product.objects.create(name=cls.product_name, price="10", created_by=cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductListViewTestCase(TestCase):
    fixtures = [
        "group-fixture.json",
        "user-fixture.json",
        "product-fixture.json",
    ]

    def test_products(self):
        response = self.client.get(
            reverse("shopapp:product_list")
        ) 
        for product in Product.objects.filter(active=True).all():
            self.assertContains(response, product.name)


class OrderDetailViewTestCase(TestCase):

    fixtures = [
        "permission-fixture.json",
        "group-fixture.json",
        "user-fixture.json",
        "product-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.promocode = "TEST"
        cls.address = "Test address"
        cls.user = User.objects.create_user(username="test", password="qwerty")
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

        self.order = Order.objects.create(user=self.user, delivery_address=self.address,  promocode=self.promocode)
        self.order.products.set(Product.objects.filter(active=True))
        self.order.save()

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order.pk})
        ) 
        response_data = response.context["object"].pk
        self.assertContains(response, self.address)
        self.assertContains(response, self.promocode)
        self.assertEqual(response_data, self.order.pk)

class OrdersExportTestCase(TestCase):

    fixtures = [
        "permission-fixture.json",
        "group-fixture.json",
        "user-fixture.json",
        "product-fixture.json",
        "order-fixture.json"
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="test", password="qwerty")
        cls.user.is_staff = True
        cls.user.save()   

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_export_orders(self):
        response = self.client.get(
            reverse("shopapp:export_orders")
        ) 

        self.assertEqual(response.status_code, 200)
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
        response_data = response.json()
        self.assertEqual(response_data["orders"], orders_data)