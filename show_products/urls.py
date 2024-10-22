from django.urls import path
from show_products.views import *

app_name = 'show_products'

urlpatterns = [
    path('', show_products, name='show_products'),
    path('dev', show_main, name='show_main'),
    path('create_product', create_product_entry, name='create_product_entry'),
    path('create_category', create_category, name='create_category'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]