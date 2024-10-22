from django.shortcuts import render, redirect
from show_products.forms import *
from show_products.models import *


# Create your views here.
def show_products(request):
    context = {
        
    }
    return render(request, "show_products.html", context)

def show_main(request):
    product_entries = Product.objects.all()
    context = {
        'product_entries': product_entries
    }

    return render(request, "main.html", context)

def create_product_entry(request):
    form = ProductEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
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