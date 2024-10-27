from django.db import models
import uuid
from django.contrib.auth.models import User
from show_products.models import Product

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True) 
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} in {self.collection.name if self.collection else 'Default Wishlist'}"