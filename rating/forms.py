from django import forms
from .models import ProductRating

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),  # Dropdown for ratings 1 to 5
            'description': forms.Textarea(attrs={'rows': 3}),
        }