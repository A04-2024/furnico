from django.urls import path
from show_products.views import *

app_name = 'show_products'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('edit_product/<str:id>', edit_product, name='edit_product'),
    path('edit_category/<str:id>', edit_category, name='edit_category'),
    path('delete_product/<str:id>', delete_product, name='delete_product'),
    path('delete_category/<str:id>', delete_category, name='delete_category'),
    path('product/<str:id>', show_product, name='show_product'),
    path('all_product', show_all_products, name='show_all_products'),
    path('all_product/<str:id>', show_category_products, name='show_category_products'),
    path('search/', search_products, name='search_products'),

    path('create_product_ajax', create_product_entry_ajax, name='create_product_entry_ajax'),
    path('create_category_ajax', create_category_ajax, name='create_category_ajax'),
    path('json_filtered/<str:id>/', show_json_filtered, name='show_json_filtered'),

    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('json_cat/', show_json_cat, name='show_json_cat'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]