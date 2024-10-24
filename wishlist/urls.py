from django.urls import path
from wishlist.views import *

app_name = 'wishlist'

urlpatterns = [
    path('add_to_wishlist/<str:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('', wishlist_view, name='wishlist'),
    path('create_collection/', create_collection, name='create_collection'),
    path('remove_wishlist/<str:wishlist_item_id>/', remove_wishlist, name='remove_wishlist'),
    path('update_collection_name/<str:collection_id>/', update_collection_name, name='update_collection_name'),
    path('delete_collection/<str:collection_id>/', delete_collection, name='delete_collection'),
]
