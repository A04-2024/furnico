from django.urls import path
from show_products.views import *

app_name = 'show_products'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('dev', show_main, name='show_main'),
]