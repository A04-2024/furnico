from django.shortcuts import render, get_object_or_404
from show_products.models import Product
from rating.forms import ProductRatingForm
from rating.models import ProductRating
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers


def show_rating(request):
    ratings = ProductRating.objects.all() 

    context = {
        'title': "Recent Review",
        'ratings': ratings  # Pass all ratings to the template
    }

    return render(request, 'rating.html', context)


@csrf_exempt
@require_POST
def add_rating_ajax(request):
    form = ProductRatingForm(request.POST)
    
    if form.is_valid():
        rating = form.save(commit=False) 
        rating.user = request.user  
        rating.save()
        return HttpResponse("CREATED", status=201)
    else:
        # Send back an error message with status 400
        error_message = ', '.join([f"{field}: {error[0]}" for field, error in form.errors.items()])
        return HttpResponse(f"Error: {error_message}", status=400)
    
def edit_rating(request, id):
    # Get the product entry
    rating = ProductRating.objects.get(pk=id)

    # Set product entry sebagai instance dari form
    form = ProductRatingForm(request.POST or None, instance=rating)

    if form.is_valid() and request.method == "POST":
        form.save() # simpan form dan kembali ke halaman awal
        return HttpResponseRedirect(reverse('rating:show_rating'))
    
    context = {'form': form}
    return render(request, "edit_rating.html", context)

def delete_rating(request, id):
    rating = ProductRating.objects.get(pk=id) # Get product berdasarkan id
    rating.delete() # hapus product
    return HttpResponseRedirect(reverse('rating:show_rating'))

def show_xml(request):
    data = ProductRating.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type='application/xml')

def show_json(request):
    data = ProductRating.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type='application/json')

def show_xml_by_id(request, id):
    data = ProductRating.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ProductRating.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
