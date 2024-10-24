from django.urls import path
from report.views import *

urlpatterns = [
    path('create_report_ajax/<int:furniture_id>/', Create_report_ajax, name='Create_report_ajax'),
    path('admin_jumlah_report_ajax/<int:furniture_id>/', Admin_jumlah_report_ajax, name='Admin_jumlah_report_ajax'),
    path('admin_list_report_furniture/<int:furniture_id>/', Admin_list_report_furniture, name='Admin_list_report_furniture'),
    path('admin_list_report/', Admin_list_report, name='Admin_list_report'),
]
