from django.urls import path
from . import views

app_name = 'ratings'
# app_name = 'show_product'

urlpatterns = [
    path('product/<uuid:id>/add/', views.add_rating, name='add_rating'),
    path('product/<uuid:rating_id>/edit', views.edit_rating, name='edit_rating'),
    path('product/<uuid:rating_id>/delete', views.delete_rating, name='delete_rating'),
    path('product/<uuid:id>/add-rating-ajax/', views.add_rating_ajax, name='add_rating_ajax'),
    path('json/', views.show_json, name='show_json'),
]