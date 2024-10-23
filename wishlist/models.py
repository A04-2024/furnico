# from django.db import models
# from django.contrib.auth.models import User  # Import User model
# import uuid

# class Collection(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User model
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class WishlistItem(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Ensure Product model exists
#     collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.product_name} in {self.collection.name if self.collection else 'Default Wishlist'}"
