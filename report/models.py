from django.db import models
from django.contrib.auth.models import User
from show_products.models import Product

# Model untuk report
class Report(models.Model):
    REASON_CHOICES = [
        ('info_error', 'Kesalahan info furniture'),
        ('image_error', 'Gambar furniture salah atau kurang jelas'),
        ('website_issue', 'Masalah pada website'),
        ('pricing_error', 'Kesalahan harga'),
        ('out_of_stock', 'Barang tidak tersedia'),
        ('slow_performance', 'Website lambat atau tidak responsif'),
        ('layout_issue', 'Tampilan website tidak rapi'),
        ('other', 'Lainnya'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Product, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    additional_info = models.TextField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report by {self.user.username} on {self.furniture.name}'

