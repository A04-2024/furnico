from django.forms import ModelForm
from rating.models import ProductRating

class ProductRatingForm(ModelForm):
    class Meta:
        model = ProductRating
        fields = ["rating", "description"]
