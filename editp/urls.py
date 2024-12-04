from django.urls import path
from . import views

from editp.views import *

app_name = 'editp'

urlpatterns = [
    path('admin_page/', views.admin_only_view, name='admin_page'),
    path('', views.edit_profile, name='edit_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
