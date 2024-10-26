from django.test import TestCase

from django.test import TestCase
from show_products.models import Categories, Product

class CategoriesModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(
            category_name="Electronics",
            unique_products=10,
            image_url="http://example.com/image.png"
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(
            category_name="Electronics",
            unique_products=10,
            image_url="http://example.com/image.png"
        )
        self.product = Product.objects.create(
            product_image="http://example.com/product_image.png",
            product_name="Smartphone",
            product_subtitle="Latest model",
            product_price=999,
            sold_this_week=100,
            people_bought=50,
            product_description="A great smartphone.",
            product_advantages="Fast, reliable, high-quality camera.",
            product_material="Aluminum",
            product_size_length=15,
            product_size_height=7,
            product_size_long=0.5,
            product_category=self.category,
            product_rating=5
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Smartphone")

from django.test import TestCase, Client
from django.urls import reverse
from show_products.models import Categories, Product

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Categories.objects.create(
            category_name="Electronics",
            unique_products=10,
            image_url="http://example.com/image.png"
        )
        self.product = Product.objects.create(
            product_image="http://example.com/product_image.png",
            product_name="Smartphone",
            product_subtitle="Latest model",
            product_price=999,
            sold_this_week=100,
            people_bought=50,
            product_description="A great smartphone.",
            product_advantages="Fast, reliable, high-quality camera.",
            product_material="Aluminum",
            product_size_length=15,
            product_size_height=7,
            product_size_long=0.5,
            product_category=self.category,
            product_rating=5
        )

    def test_show_main_view(self):
        response = self.client.get(reverse('show_products:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main.html")

    def test_show_all_products_view(self):
        response = self.client.get(reverse('show_products:show_all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_products.html")

    def test_show_category_products_view(self):
        response = self.client.get(reverse('show_products:show_category_products', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_category.html")

    def test_show_product_view(self):
        response = self.client.get(reverse('show_products:show_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_page.html")

    def test_show_nonexistent_product_view(self):
        response = self.client.get(reverse('show_products:show_product', args=['nonexistent_id']))
        self.assertEqual(response.status_code, 404)

from django.test import TestCase, Client
from show_products.models import Categories

class AJAXViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Categories.objects.create(
            category_name="Electronics",
            image_url="http://example.com/image.png"
        )

    def test_create_product_entry_ajax(self):
        response = self.client.post(reverse('show_products:create_product_entry_ajax'), {
            "product_image": "http://example.com/product_image.png",
            "product_name": "Smartphone",
            "product_subtitle": "Latest model",
            "product_price": 999,
            "sold_this_week": 100,
            "people_bought": 50,
            "product_description": "A great smartphone.",
            "product_advantages": "Fast, reliable, high-quality camera.",
            "product_material": "Aluminum",
            "product_size_length": 15,
            "product_size_height": 7,
            "product_size_long": 0.5,
            "product_category": str(self.category.id)
        })
        self.assertEqual(response.status_code, 201)

    def test_create_category_ajax(self):
        response = self.client.post(reverse('show_products:create_category_ajax'), {
            "category_name": "Home Appliances",
            "image_url": "http://example.com/home_appliance_image.png"
        })
        self.assertEqual(response.status_code, 201)

