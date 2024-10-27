from django.urls import path
from wishlist.views import *

app_name = 'wishlist'

urlpatterns = [
    path('add-to-wishlist/<str:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<str:product_id>/', remove_wishlist, name='remove_wishlist'),
    path('', wishlist_view, name='wishlist'),
    path('wishlist-json/', wishlist_json_view, name='wishlist_json'),
    path('create-collection/', create_collection, name='create_collection'),
    path('update-collection-name/<int:collection_id>/', update_collection_name, name='update_collection_name'),
    path('delete-collection/<int:collection_id>/', delete_collection, name='delete_collection'),
]