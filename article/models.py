from django.db import models
from django.contrib.auth.models import User
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.name} on {self.article}'