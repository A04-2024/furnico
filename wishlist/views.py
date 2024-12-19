from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import WishlistItem, Collection
from show_products.models import Product
from .forms import CollectionForm
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        collection_id = data.get('collection_id')
        if collection_id:
            collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        else:
            collection, created = Collection.objects.get_or_create(user=request.user, name="Semua Wishlist")
        WishlistItem.objects.create(product=product, collection=collection)
        return JsonResponse({'success': True})

    collections = Collection.objects.filter(user=request.user)
    return render(request, 'add_to_wishlist.html', {'product': product, 'collections': collections})

@csrf_exempt
def wishlist_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    collections = Collection.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'collections': collections})

def wishlist_json_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    collections = Collection.objects.filter(user=request.user).prefetch_related('wishlistitem_set__product')

    wishlist_data = []
    for collection in collections:
        collection_data = {
            'collection_id': collection.id,
            'collection_name': collection.name,
            'items': [
                {
                    'product_id': item.product.id,
                    'product_name': item.product.product_name
                }
                for item in collection.wishlistitem_set.all()
            ]
        }
        wishlist_data.append(collection_data)

    return JsonResponse({'status':'success','collections': wishlist_data})

@csrf_exempt
def create_collection(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            collection_name = data.get('collection_name')
            form = CollectionForm({'name': collection_name})

            if form.is_valid():
                collection = form.save(commit=False)
                collection.user = request.user
                collection.save()

                return JsonResponse({
                    'success': True,
                    'collection': {
                        'id': collection.id,
                        'name': collection.name
                    }
                })

            return JsonResponse({'success': False, 'errors': form.errors})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def update_collection_name(request, collection_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    collection = get_object_or_404(Collection, id=collection_id, user=request.user)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            collection_name = data.get('collection_name')
            form = CollectionForm({'name': collection_name}, instance=collection)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'collection': {
                        'id': collection.id,
                        'name': collection.name
                    }
                })
            return JsonResponse({'success': False, 'errors': form.errors})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def delete_collection(request, collection_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    collection = get_object_or_404(Collection, id=collection_id, user=request.user)

    if collection.name == "Semua Wishlist":
        return JsonResponse({'success': False, 'message': 'Cannot delete default collection'})

    default_collection, created = Collection.objects.get_or_create(user=request.user, name="Semua Wishlist")

    collection_items = collection.wishlistitem_set.all()
    collection_items.update(collection=default_collection)
    collection.delete()

    return JsonResponse({'success': True})

@csrf_exempt
def remove_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated or logged in'})

    wishlist_item = get_object_or_404(WishlistItem, product__id=product_id, collection__user=request.user)
    wishlist_item.delete()
    return JsonResponse({'success': True})
