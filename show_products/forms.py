from django.forms import ModelForm
from show_products.models import *

class ProductEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "product_subtitle", "product_price", "product_image", "sold_this_week", "people_bought", "product_description", "product_advantages", "product_material", "product_size_length", "product_size_height", "product_size_long", "product_category"] 

class CategoryEntryForm(ModelForm):
    class Meta:
        model = Categories
        fields = ["category_name", "image_url"]