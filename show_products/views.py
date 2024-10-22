from django.shortcuts import render, redirect, reverse
from show_products.forms import *
from show_products.models import *

# returns data in xml and json
from django.http import HttpResponse, HttpResponseRedirect
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

def edit_product(request, id):
    # Get product entry berdasarkan id
    product = Product.objects.get(pk = id)
    category = product.product_category

    # Set product entry sebagai instance dari form
    form = ProductEntryForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        product_entry = form.save()  # Simpan produk baru

        # Akses kategori terkait dan tambahkan 1 ke jumlah_product
        new_category = product_entry.product_category
        if (category != new_category):
            category.unique_products -= 1
        category.save()  # Simpan perubahan kategori
        return HttpResponseRedirect(reverse('show_products:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def edit_category(request, id):
    # Get category berdasarkan id
    category = Categories.objects.get(pk = id)

    # Set category sebagai instance dari form
    form = CategoryEntryForm(request.POST or None, instance=category)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('show_products:show_main'))

    context = {'form': form}
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