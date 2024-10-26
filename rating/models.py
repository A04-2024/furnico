from django.db import models
from django.contrib.auth.models import User
from show_products.models import Product
import uuid

class ProductRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()

    def __str__(self):
        return f'{self.product.product_name} - {self.rating} by {self.user.username}'
