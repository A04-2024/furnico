from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import EditProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = EditProfile
        fields = ['phone_number', 'profile_picture']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User