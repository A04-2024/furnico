from django.urls import path
from rating.views import show_rating, edit_rating, delete_rating, add_rating_ajax, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'rating'

urlpatterns = [
    path('', show_rating, name='show_rating'),
    path('edit-rating/<uuid:id>', edit_rating, name='edit_rating'),
    path('delete/<uuid:id>', delete_rating, name='delete_rating'),
    path('create-rating-ajax', add_rating_ajax, name='add_rating_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]