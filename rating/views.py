from django.shortcuts import render, get_object_or_404, redirect

from rating.serializers import ProductRatingSerializer
from .models import ProductRating
from .forms import ProductRatingForm
from show_products.models import Product 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.core import serializers

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

    new_rating = ProductRating(
        rating=rating, 
        description=description, 
        user=user, 
        product=product
    )
    new_rating.save()

    return HttpResponse(b"CREATED", status=201)
