from django.shortcuts import render, redirect
from show_products.forms import *
from show_products.models import *

# returns data in xml and json
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_products(request):
    context = {
        
    }
    return render(request, "show_products.html", context)

def show_main(request):
    product_entries = Product.objects.all()
    categories = Categories.objects.all()
    context = {
        'product_entries': product_entries,
        'categories': categories
    }

    return render(request, "main.html", context)

def create_product_entry(request):
    form = ProductEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save()  # Simpan produk baru

        # Akses kategori terkait dan tambahkan 1 ke jumlah_product
        category = product_entry.product_category
        category.unique_products += 1
        category.save()  # Simpan perubahan kategori

        return redirect('show_products:show_main')
    
    context = {'form': form}
    return render(request, "create_product_entry.html", context)

def create_category(request):
    form = CategoryEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('show_products:show_main')

    context = {'form': form}
    return render(request, "create_category.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
