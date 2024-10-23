from django.urls import path
from .views import show_rating 

app_name = 'rating' 

urlpatterns = [
    path('products/<uuid:product_id>/ratings/', show_rating, name='show_rating'),
]
