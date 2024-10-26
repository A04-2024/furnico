from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    # path('', report_view, name='report'),
    path('create_report/<str:product_id>', create_report_ajax, name='create_report'),
    path('admin_jumlah_report_ajax/<str:product_id>', admin_jumlah_report_ajax, name='admin_jumlah_report_ajax'),
    path('admin_list_report_furniture/<str:product_id>', admin_list_report_furniture, name='admin_list_report_furniture'),
    path('admin_list_report/', admin_list_report, name='admin_list_report'),
]
