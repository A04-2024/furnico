from django.db import models
import uuid

# Create your models here.

class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255)
    unique_products = 0

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_image = models.ImageField()
    product_name = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255)
    sold_this_week = models.IntegerField()
    people_bought = models.IntegerField()
    product_description = models.TextField()
    product_advantages = models.TextField()
    product_material = models.CharField(max_length=255)
    product_size_length = models.IntegerField()
    product_size_height = models.IntegerField()
    product_size_long = models.IntegerField()
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE)