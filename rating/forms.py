from django.forms import ModelForm
from rating.models import ProductRating
from django.utils.html import strip_tags

class ProductRatingForm(ModelForm):
    class Meta:
        model = ProductRating
        fields = ["rating", "description"]

    def clean_name(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
