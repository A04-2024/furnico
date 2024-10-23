from django.db import models
from django.contrib.auth.models import User

# Model Report untuk menyimpan laporan pengguna tentang furniture
class Report(models.Model):
    REASON_CHOICES = [
        ('incorrect_info', 'Incorrect Information'),
        ('wrong_image', 'Wrong Image'),
        ('site_issue', 'Website Issue'),
        ('other', 'Other'),
    ]

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)  # Alasan laporan
    additional_info = models.TextField(blank=True, null=True)  # Kolom untuk keterangan tambahan
    report_image = models.ImageField(upload_to='report_images/', blank=True, null=True)  # Menambahkan field untuk gambar
    report_date = models.DateTimeField(auto_now_add=True)  # Tanggal laporan otomatis