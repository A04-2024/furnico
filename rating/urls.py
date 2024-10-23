from django.urls import path
from rating.views import show_rating

app_name = 'rating'

urlpatterns = [
    path('', show_rating, name='show_rating'),
]