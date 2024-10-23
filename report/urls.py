from django.urls import path
from report.views import *

urlpatterns = [
    # URL untuk halaman laporan
    path('report/<int:furniture_id>/', create_report, name='create_report'),
    path('reports/', report_list, name='report_list'),  # URL untuk admin melihat semua laporan
]
