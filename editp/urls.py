from django.urls import path
from . import views

from editp.views import *

app_name = 'editp'

urlpatterns = [
    path('', views.edit_profile, name='edit_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
