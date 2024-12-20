import json
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from rating.serializers import ProductRatingSerializer
from .models import ProductRating
from .forms import ProductRatingForm
from show_products.models import Product 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.middleware.csrf import get_token


from rest_framework.renderers import JSONRenderer

def add_rating(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product  
            rating.user = request.user  
            rating.save()
            return redirect('show_products:show_product', id=product.id)
    else:
        form = ProductRatingForm()
    
    return render(request, 'add_rating.html', {'form': form, 'product': product})

def edit_rating(request, rating_id):
    rating = get_object_or_404(ProductRating, id=rating_id)
    
    if rating.user != request.user:
        return redirect('show_products:show_product', id=rating.product.id)
    
    if request.method == 'POST':
        form = ProductRatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('show_products:show_product', id=rating.product.id)
    else:
        form = ProductRatingForm(instance=rating)

    return render(request, 'edit_rating.html', {'form': form, 'product': rating.product})

def delete_rating(request, rating_id):
    rating = get_object_or_404(ProductRating, id=rating_id)
        
    if rating.user == request.user:
        product_id = rating.product.id
        rating.delete()
        return redirect('show_products:show_product', id=product_id)

    return redirect('show_products:show_product', id=rating.product.id)

def show_json(request, id):
    ratings = ProductRating.objects.filter(product_id=id)
    data = [
        {
            "id": rating.id,
            "user": {"username": rating.user.username},
            "rating": rating.rating,
            "description": rating.description,
            "is_owner": rating.user == request.user,
        }
        for rating in ratings
    ]
    return JsonResponse(data, safe=False)

def show_json_by_id(request, rating_id, product_id):
    product = get_object_or_404(Product, id=product_id)
    rating = ProductRating.objects.filter(pk=rating_id, product=product)
    return HttpResponse(serializers.serialize("json", rating), content_type="application/json")

@csrf_exempt
@require_POST
def add_rating_ajax(request, id):
    rating = request.POST.get("rating")
    description = request.POST.get("description")
    product = get_object_or_404(Product, pk=id)
    user = request.user

    # Validation for rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return JsonResponse({
                "status": "error",
                "message": "Rating must be between 1 and 5."
            }, status=400)
    except (ValueError, TypeError):
        return JsonResponse({
            "status": "error",
            "message": "Invalid rating value. It must be an integer between 1 and 5."
        }, status=400)

    # Validation for description
    if not description or len(description.strip()) == 0:
        return JsonResponse({
            "status": "error",
            "message": "Description cannot be empty."
        }, status=400)

    new_rating = ProductRating(
        rating=rating, 
        description=description, 
        user=user, 
        product=product
    )
    new_rating.save()

    # update product rating average for the product card
    product.product_rating = calculate_average_rating(product)


    # Return the updated average rating in the response
    return JsonResponse({
        "status": "success",
        "updated_average": product.product_rating,
        "rating": new_rating.rating,
        "description": new_rating.description
    }, status=201)

def calculate_average_rating(product):
    ratings = product.ratings.all()
    if ratings.exists():
        return round(ratings.aggregate(Avg('rating'))['rating__avg'])
    return 0

@receiver(post_save, sender=ProductRating)
@receiver(post_delete, sender=ProductRating)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    product.product_rating = calculate_average_rating(product)
    product.save()


# FLUTTER
@csrf_exempt
def create_rating_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Get the product instance using the product_id from the URL
        product = get_object_or_404(Product, pk=id)
        user = request.user
        # Create a new rating
        new_rating = ProductRating.objects.create(
            rating=data['rating'],
            description=data['description'],
            user=user,
            product=product
        )
        new_rating.save()

        # Create the JSON response in the desired format
        ratings = ProductRating.objects.filter(product=product)

        ratings_data = [
            {
                "id": str(product.id),
                "user": {
                    "username": rating.user.username  
                },
                "rating": rating.rating,
                "description": rating.description,
                "is_owner": rating.user == request.user
            }
            for rating in ratings
        ]

        return JsonResponse(ratings_data, safe=False, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})