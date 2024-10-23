from django.forms import ModelForm
from wishlist.models import *
from django import forms

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name"]