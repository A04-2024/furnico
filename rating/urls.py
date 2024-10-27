from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('product/<uuid:id>/add/', views.add_rating, name='add_rating'),
    path('rating/<uuid:rating_id>/edit/', views.edit_rating, name='edit_rating'),
    path('rating/<uuid:rating_id>/delete/', views.delete_rating, name='delete_rating'),
]