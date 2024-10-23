from django.db import models

class ProductRating(models.Model):
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()