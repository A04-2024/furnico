from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
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
    
    def clean(self):
        # Ensuring the rating is between 1 and 5
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
