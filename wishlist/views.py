# from django.shortcuts import render, redirect, get_object_or_404
# from .models import WishlistItem, Collection, Product
# from django.contrib.auth.decorators import login_required
# # Correct the import by specifying the correct app where the Product model is located
# from .models import WishlistItem, Collection
# from wishlist.models import Product  # Assuming Product is in the 'products' app


# @login_required
# def wishlist_view(request):
#     collections = Collection.objects.filter(user=request.user)
#     default_items = WishlistItem.objects.filter(collection__isnull=True, collection__user=request.user)

#     return render(request, 'wishlist.html', {
#         'collections': collections,
#         'default_items': default_items,
#     })

# @login_required
# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     collection_id = request.POST.get('collection_id')
    
#     if collection_id:
#         collection = get_object_or_404(Collection, id=collection_id, user=request.user)
#     else:
#         collection = None

#     WishlistItem.objects.create(product=product, collection=collection)
#     return redirect('wishlist_view')

# @login_required
# def remove_from_wishlist(request, item_id):
#     wishlist_item = get_object_or_404(WishlistItem, id=item_id, collection__user=request.user)
#     wishlist_item.delete()
#     return redirect('wishlist_view')
