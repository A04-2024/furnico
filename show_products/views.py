from django.shortcuts import render, redirect, reverse
from show_products.forms import *
from show_products.models import *
from report.forms import ReportForm

# returns data in xml and json
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# ajax
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

# Create your views here.
def show_products(request):
    context = {
        
    }
    return render(request, "show_products.html", context)

@login_required(login_url='profile/login/')
def show_main(request):
    # product_entries = Product.objects.all()
    categories = Categories.objects.all()
    context = {
        # 'product_entries': product_entries,
        'categories': categories
    }

    return render(request, "main.html", context)

def show_all_products(request):
    product_entries = Product.objects.all()
    categories = Categories.objects.all()
    context = {
        'product_entries': product_entries,
        'categories': categories
    }

    return render(request, "all_products.html", context)

def show_category_products(request, id):
    categories = Categories.objects.all()
    filtered_category = Categories.objects.get(pk=id)

    # Filter product entries based on the selected category
    product_entries = Product.objects.filter(product_category=filtered_category)

    context = {
        'product_entries': product_entries,
        'filtered_category': filtered_category,
        'categories': categories
    }

    return render(request, "show_category.html", context)

def show_xml(request):
    # data = Product.objects.all()
    data = Product.objects.all() # ganti jadi .filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    user = request.user
    products = Product.objects.all()

    # Create a custom list of dictionaries with the data and the extra field
    product_list = []
    for product in products:
        product_dict = {
            "model": "show_products.product",
            "pk": str(product.pk),  # Convert UUID to string
            "fields": {
                "product_image": product.product_image,
                "product_name": product.product_name,
                "product_subtitle": product.product_subtitle,
                "product_price": product.product_price,
                "sold_this_week": product.sold_this_week,
                "people_bought": product.people_bought,
                "product_description": product.product_description,
                "product_advantages": product.product_advantages,
                "product_material": product.product_material,
                "product_size_length": product.product_size_length,
                "product_size_height": product.product_size_height,
                "product_size_long": product.product_size_long,
                "product_category": str(product.product_category.id) if product.product_category else None,
                "product_rating": product.product_rating,
                "store_name": product.store_name,
                "store_address": product.store_address,
                "in_wishlist": product.is_in_wishlist(user) if user.is_authenticated else False,
            }
        }
        product_list.append(product_dict)

    # Use JsonResponse to return the custom list
    return JsonResponse(product_list, safe=False)

def show_json_cat(request):
    # data = Product.objects.all()
    data = Categories.objects.all() # ganti jadi .filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_cat_get(request, id):
    data = Categories.objects.filter(pk=id)  
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_json_filtered(request, id):
    category = Categories.objects.get(pk=id)
    products = Product.objects.filter(product_category=category)
    user = request.user

    product_list = []
    for product in products:
        product_dict = {
            "model": "show_products.product",
            "pk": str(product.pk),  # Convert UUID to string
            "fields": {
                "product_image": product.product_image,
                "product_name": product.product_name,
                "product_subtitle": product.product_subtitle,
                "product_price": product.product_price,
                "sold_this_week": product.sold_this_week,
                "people_bought": product.people_bought,
                "product_description": product.product_description,
                "product_advantages": product.product_advantages,
                "product_material": product.product_material,
                "product_size_length": product.product_size_length,
                "product_size_height": product.product_size_height,
                "product_size_long": product.product_size_long,
                "product_category": str(product.product_category.id) if product.product_category else None,
                "product_rating": product.product_rating,
                "store_name": product.store_name,
                "store_address": product.store_address,
                "in_wishlist": product.is_in_wishlist(user) if user.is_authenticated else False,
            }
        }
        product_list.append(product_dict)

    # Use JsonResponse to return the custom list
    return JsonResponse(product_list, safe=False)

def show_xml_by_id(request, id):
    # data = Product.objects.filter(pk=id)
    data = Product.objects.filter(pk=id) 
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    # data = Product.objects.filter(pk=id)
    product = Product.objects.get(pk=id) 
    user = request.user

    product_list = []
    product_dict = {
        "model": "show_products.product",
        "pk": str(product.pk),  # Convert UUID to string
        "fields": {
            "product_image": product.product_image,
            "product_name": product.product_name,
            "product_subtitle": product.product_subtitle,
            "product_price": product.product_price,
            "sold_this_week": product.sold_this_week,
            "people_bought": product.people_bought,
            "product_description": product.product_description,
            "product_advantages": product.product_advantages,
            "product_material": product.product_material,
            "product_size_length": product.product_size_length,
            "product_size_height": product.product_size_height,
            "product_size_long": product.product_size_long,
            "product_category": str(product.product_category.id) if product.product_category else None,
            "product_rating": product.product_rating,
            "store_name": product.store_name,
            "store_address": product.store_address,
            "in_wishlist": product.is_in_wishlist(user) if user.is_authenticated else False,
        }
    }
    product_list.append(product_dict)

    # Use JsonResponse to return the custom list
    return JsonResponse(product_list, safe=False)

def edit_product(request, id):
    product = Product.objects.get(pk = id)
    category = product.product_category
    categories = Categories.objects.all()

    form = ProductEntryForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save()  
        new_category = product_entry.product_category
        if (category != new_category):
            category.unique_products -= 1
        category.save()
        return HttpResponseRedirect(reverse('show_products:show_main'))

    context = {'form': form,
               'product': product,
               'categories':categories}
    return render(request, "edit_product.html", context)

def edit_category(request, id):
    # Get category berdasarkan id
    category = Categories.objects.get(pk = id)
    categories = Categories.objects.all()

    # Set category sebagai instance dari form
    form = CategoryEntryForm(request.POST or None, instance=category)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('show_products:show_main'))

    context = {'form': form,
               'category': category}
    return render(request, "edit_category.html", context)

def delete_product(request, id):
    # Get product berdasarkan id
    product = Product.objects.get(pk = id)
    # Hapus product
    product.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('show_products:show_main'))

def delete_category(request, id):
    # Get category berdasarkan id
    category = Categories.objects.get(pk = id)
    # Hapus category
    category.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('show_products:show_main'))


def show_product(request, id):
    product = Product.objects.get(pk = id)
    product.in_wishlist = product.is_in_wishlist(request.user)
    form = ReportForm()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, "product_page.html", context)

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        product_name__icontains=query
    ) | Product.objects.filter(
        product_subtitle__icontains=query
    )
    product_data = list(products.values('pk', 'product_name', 'product_subtitle', 'product_image', 'product_price'))
    return JsonResponse({'products': product_data})

@csrf_exempt
@require_POST
def create_product_entry_ajax(request):
    product_image = request.POST.get("product_image")
    product_name = request.POST.get("product_name")
    product_subtitle = request.POST.get("product_subtitle")
    product_price = request.POST.get("product_price")
    sold_this_week = request.POST.get("sold_this_week")
    people_bought = request.POST.get("people_bought")
    product_description = request.POST.get("product_description")
    product_advantages = request.POST.get("product_advantages")
    product_material = request.POST.get("product_material")
    product_size_length = request.POST.get("product_size_length")
    product_size_height = request.POST.get("product_size_height")
    product_size_long = request.POST.get("product_size_long")
    product_category = request.POST.get("product_category")

    new_product = Product(
        product_image=product_image,
        product_name=product_name,
        product_subtitle=product_subtitle,
        product_price=product_price,
        sold_this_week=sold_this_week,
        people_bought=people_bought,
        product_description=product_description,
        product_advantages=product_advantages,
        product_material=product_material,
        product_size_length=product_size_length,
        product_size_height=product_size_height,
        product_size_long=product_size_long,
        product_category=Categories.objects.get(id=product_category),
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def create_category_ajax(request):
    category_name = request.POST.get("category_name")
    image_url = request.POST.get("image_url")

    new_category = Categories(
        category_name=category_name,
        image_url=image_url
    )

    new_category.save()

    return HttpResponse(b"CREATED", status=201)

def search_products(request):
    query = request.GET.get('q', '')
    offset = int(request.GET.get('offset', 0))  # Default to 0
    limit = int(request.GET.get('limit', 10))  # Default to 10

    # Search logic (replace with your actual logic)
    products = Product.objects.filter(product_name__icontains=query)[offset:offset + limit]
    data = {'products': list(products.values())}
    return JsonResponse(data)


# ==============================================
# FLUTTERRR 
# ==============================================
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        print(request.body)
        category = Categories.objects.get(id=data["product_category"])
        print(category.category_name)
        new_product = Product.objects.create(
                product_image=data["product_image"],
                product_name=data["product_name"],
                product_subtitle=data["product_subtitle"],
                product_price=int(data["product_price"]),
                sold_this_week=int(data["sold_this_week"]),
                people_bought=int(data["people_bought"]),
                product_description=data["product_description"],
                product_advantages=data["product_advantages"],
                product_material=data["product_material"],
                product_size_length=int(data["product_size_length"]),
                product_size_height=int(data["product_size_height"]),
                product_size_long=int(data["product_size_long"]),
                product_category=category,
                store_name=data["store_name"],
                store_address=data["store_address"],
            )

        print(new_product)
        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def create_category_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_category = Categories.objects.create(
            image_url=data["category_image"],
            category_name=data["category_name"],
        )

        new_category.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_category_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        category = Categories.objects.get(id=data["category_id"])
        category.delete()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_product_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        product = Product.objects.get(id=data["product_id"])
        product.delete()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_product_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        product = Product.objects.get(id=data["product_id"])
        category = Categories.objects.get(id=data["product_category"])

        product.product_image=data["product_image"]
        product.product_name=data["product_name"]
        product.product_subtitle=data["product_subtitle"]
        product.product_price=int(data["product_price"])
        product.sold_this_week=int(data["sold_this_week"])
        product.people_bought=int(data["people_bought"])
        product.product_description=data["product_description"]
        product.product_advantages=data["product_advantages"]
        product.product_material=data["product_material"]
        product.product_size_length=int(data["product_size_length"])
        product.product_size_height=int(data["product_size_height"])
        product.product_size_long=int(data["product_size_long"])
        product.product_category=category
        product.store_name=data["store_name"]
        product.store_address=data["store_address"]

        product.save()
        print(product)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
@csrf_exempt
def edit_category_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        category = Categories.objects.get(id=data["category_id"])

        category.image_url=data["category_image"]
        category.category_name=data["category_name"]

        category.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)