from django.shortcuts import render, get_object_or_404
from .models import ProductRating, Product

def show_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    ratings = ProductRating.objects.filter(product=product).order_by('-created_at')

    context = {
        'product': product,
        'ratings': ratings
    }

    return render(request, "rating.html", context)
