# serializers.py
from rest_framework import serializers
from .models import ProductRating, Product
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'product_image',
            'product_name',
            'product_subtitle',
            'product_price',
            'sold_this_week',
            'people_bought',
            'product_description',
            'product_advantages',
            'product_material',
            'product_size_length',
            'product_size_height',
            'product_size_long',
            'product_category'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Adjust fields as per your requirements

class ProductRatingSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested product details
    user = UserSerializer(read_only=True)  # Nested user details

    class Meta:
        model = ProductRating
        fields = ['id', 'product', 'user', 'rating', 'description']
