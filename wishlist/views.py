from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WishlistItem, Collection
from show_products.models import Product
from .forms import CollectionForm
from django.contrib.auth.models import User

def mock_user():
    user, created = User.objects.get_or_create(username='mockuser', id=1)
    return user

# @login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = mock_user()
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        if collection_id:
            collection = get_object_or_404(Collection, id=collection_id, user=user)
        else:
            collection, created = Collection.objects.get_or_create(user=user, name="Semua Wishlist")
        
        WishlistItem.objects.create(product=product, collection=collection)
        return redirect('wishlist:wishlist') 
    
    collections = Collection.objects.filter(user=user)
    return render(request, 'add_to_wishlist.html', {'product': product, 'collections': collections})


# @login_required
def wishlist_view(request):
    user = mock_user()
    collections = Collection.objects.filter(user=user)
    return render(request, 'wishlist.html', {'collections': collections})


# @login_required
def create_collection(request):
    user = mock_user()
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = user
            collection.save()
            return redirect('wishlist:wishlist')  
    else:
        form = CollectionForm()
    return render(request, 'create_collection.html', {'form': form})

# @login_required
def remove_wishlist(request, wishlist_item_id):
    user = mock_user()
    wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id, collection__user=user)
    wishlist_item.delete()
    return redirect('wishlist:wishlist')

# @login_required
def update_collection_name(request, collection_id):
    user = mock_user()
    collection = get_object_or_404(Collection, id=collection_id, user=user)

    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('wishlist:wishlist')
    else:
        form = CollectionForm(instance=collection)
    
    return render(request, 'update_collection.html', {'form': form, 'collection': collection})

# @login_required
def delete_collection(request, collection_id):
    user = mock_user()
    collection = get_object_or_404(Collection, id=collection_id, user=user)

    if collection.name == "Semua Wishlist":
        return redirect('wishlist:wishlist')

    default_collection, created = Collection.objects.get_or_create(user=user, name="Semua Wishlist")

    collection_items = collection.wishlistitem_set.all()
    collection_items.update(collection=default_collection)

    collection.delete()

    return redirect('wishlist:wishlist')