from django.contrib import admin
from .models import Furniture, Report

# Menampilkan model Furniture di admin panel
@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

# Menampilkan model Report di admin panel
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('furniture', 'user', 'reason', 'report_date', 'report_image')
    list_filter = ('reason', 'report_date')
    search_fields = ('furniture_name', 'user_username')