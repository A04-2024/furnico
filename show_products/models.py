from django.db import models
import uuid
# Create your models here.

class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255)
    unique_products = models.PositiveIntegerField(default=0)
    image_url = models.CharField(max_length=10000)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_image = models.CharField(max_length=10000)
    product_name = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255)
    product_price = models.PositiveIntegerField()
    sold_this_week = models.PositiveIntegerField()
    people_bought = models.PositiveIntegerField()
    product_description = models.TextField()
    product_advantages = models.TextField()
    product_material = models.CharField(max_length=255)
    product_size_length = models.PositiveIntegerField()
    product_size_height = models.PositiveIntegerField()
    product_size_long = models.PositiveIntegerField()
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_rating = models.PositiveSmallIntegerField()

    def is_in_wishlist(self, user):
        from wishlist.models import WishlistItem
        return WishlistItem.objects.filter(product = self, collection__user = user).exists()