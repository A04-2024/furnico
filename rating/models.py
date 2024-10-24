from django.db import models
from django.contrib.auth.models import User 
import uuid
from show_products.models import Product  

class ProductRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    # product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    rating = models.PositiveSmallIntegerField()  
    description = models.TextField()  