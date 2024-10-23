from django.db import models
from django.contrib.auth.models import User 
from uuid import uuid4
from show_products.models import Product  

class ProductRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    rating = models.PositiveSmallIntegerField()  
    description = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  