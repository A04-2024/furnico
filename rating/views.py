from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import ProductRating
from .forms import ProductRatingForm
from show_products.models import Product 

# @login_required
def add_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product  
            rating.user = request.user  
            rating.save()
            return redirect('show_products:show_product', product_id=product.id)
    else:
        form = ProductRatingForm()
    
    return render(request, 'add_rating.html', {'form': form, 'product': product})

# @login_required
def edit_rating(request, rating_id):
    rating = get_object_or_404(ProductRating, id=rating_id)
    
    if rating.user != request.user:
        return redirect('show_products:show_product', product_id=rating.product.id)
    
    if request.method == 'POST':
        form = ProductRatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('show_products:show_product', product_id=rating.product.id)
    else:
        form = ProductRatingForm(instance=rating)

    return render(request, 'edit_rating.html', {'form': form, 'product': rating.product})

# @login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(ProductRating, id=rating_id)
    
    if rating.user != request.user:
        return redirect('show_products:show_product', product_id=rating.product.id)
    
    if request.method == 'POST':
        product_id = rating.product.id
        rating.delete()
        return redirect('show_products:show_product', product_id=product_id)

    return render(request, 'delete_rating.html', {'rating': rating, 'product': rating.product})
