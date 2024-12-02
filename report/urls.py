from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('create_report/<str:id>/', create_report_ajax, name='create_report'),
    path('admin_list_report_furniture/<str:id>/', admin_list_report_furniture, name='admin_list_report_furniture'),
    path('admin_list_report/', admin_list_report, name='admin_list_report'),
]
