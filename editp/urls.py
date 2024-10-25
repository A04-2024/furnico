from django.urls import path
from . import views

from editp.views import register, login_user

urlpatterns = [
    path('', views.edit_profile, name='edit_profile'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
]
