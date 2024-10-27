from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import WishlistItem, Collection
from show_products.models import Product, Categories
import json

class WishlistFeatureTests(TestCase):

    def setUp(self):
        # Initialize Client, User, Category, Product, and Default Collection
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.category = Categories.objects.create(category_name="Alat", unique_products=5, image_url="http://example.com/electronics.jpg")
        self.product = Product.objects.create(
            product_image="http://example.com/product.jpg",
            product_name="Kursi",
            product_subtitle="Latest Model",
            product_price=999,
            sold_this_week=20,
            people_bought=100,
            product_description="Awet dan nyaman",
            product_advantages="Kuat, nyaman, tahan lama.",
            product_material="Aluminum",
            product_size_length=150,
            product_size_height=70,
            product_size_long=10,
            product_category=self.category,
            product_rating=5
        )
        self.default_collection = Collection.objects.create(user=self.user, name="Semua Wishlist")

    def test_add_to_wishlist_default_collection(self):
        # Add product to default wishlist
        response = self.client.post(reverse('wishlist:add_to_wishlist', args=[self.product.id]),
                                    json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WishlistItem.objects.filter(product=self.product, collection=self.default_collection).exists())

    def test_add_to_wishlist_custom_collection(self):
        # Create custom collection and add product to it
        custom_collection = Collection.objects.create(user=self.user, name="Favorites")
        response = self.client.post(reverse('wishlist:add_to_wishlist', args=[self.product.id]),
                                    json.dumps({'collection_id': custom_collection.id}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WishlistItem.objects.filter(product=self.product, collection=custom_collection).exists())

    def test_view_wishlist(self):
        # Ensure that the wishlist page loads correctly with collections
        response = self.client.get(reverse('wishlist:wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')
        self.assertIn('collections', response.context)

    def test_wishlist_json_view(self):
        # Add product to wishlist and check JSON response structure
        WishlistItem.objects.create(product=self.product, collection=self.default_collection)
        response = self.client.get(reverse('wishlist:wishlist_json'))
        self.assertEqual(response.status_code, 200)
        wishlist_data = response.json()['collections']
        self.assertEqual(wishlist_data[0]['collection_name'], "Semua Wishlist")
        self.assertEqual(wishlist_data[0]['items'][0]['product_name'], "Kursi")

    def test_create_collection(self):
        # Test creating a new collection
        response = self.client.post(reverse('wishlist:create_collection'),
                                    json.dumps({'collection_name': 'Holiday Gifts'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Collection.objects.filter(user=self.user, name='Holiday Gifts').exists())

    def test_update_collection_name(self):
        # Test updating a collection name
        collection = Collection.objects.create(user=self.user, name="Old Collection")
        response = self.client.post(reverse('wishlist:update_collection_name', args=[collection.id]),
                                    json.dumps({'collection_name': 'Updated Collection'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        collection.refresh_from_db()
        self.assertEqual(collection.name, 'Updated Collection')

    def test_delete_collection_and_transfer_items(self):
        # Create a collection, add product to it, delete collection, and verify items are transferred to default collection
        custom_collection = Collection.objects.create(user=self.user, name="Temporary Collection")
        wishlist_item = WishlistItem.objects.create(product=self.product, collection=custom_collection)

        response = self.client.post(reverse('wishlist:delete_collection', args=[custom_collection.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Collection.objects.filter(id=custom_collection.id).exists())
        self.assertTrue(WishlistItem.objects.filter(id=wishlist_item.id, collection=self.default_collection).exists())

    def test_cannot_delete_default_collection(self):
        # Attempt to delete the default collection and verify failure
        response = self.client.post(reverse('wishlist:delete_collection', args=[self.default_collection.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Collection.objects.filter(id=self.default_collection.id).exists())
        self.assertIn('Cannot delete default collection', response.json()['message'])

    def test_remove_item_from_wishlist(self):
        # Add product to wishlist, remove it, and verify deletion
        wishlist_item = WishlistItem.objects.create(product=self.product, collection=self.default_collection)
        response = self.client.post(reverse('wishlist:remove_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(WishlistItem.objects.filter(id=wishlist_item.id).exists())
