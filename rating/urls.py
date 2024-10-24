from django.urls import path
from rating.views import show_rating, create_rating, show_xml, show_json, show_json_by_id, show_xml_by_id, edit_rating

app_name = 'rating'

urlpatterns = [
    path('', show_rating, name='show_rating'),
    path('create-rating', create_rating, name='create_rating'),
    path('edit-rating/<uuid:id>', edit_rating, name='edit_rating'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]