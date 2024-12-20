from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('admin_list_report_furniture/<str:id>/', admin_list_report_furniture, name='admin_list_report_furniture'),
    path('admin_list_report/', admin_list_report, name='admin_list_report'),
    path('get_filtered_reports_json/', get_filtered_reports_json, name='get_filtered_reports_json'),
    path('get_report_data/<int:report_id>/', get_report_data, name='get_report_data'),
    path('create_report/<str:id>/', create_report_ajax, name='create_report'),
    path('edit_report_ajax/', edit_report_ajax, name='edit_report_ajax'),
    path('delete_report_ajax/<int:report_id>/', delete_report_ajax, name='delete_report_ajax'),

    # Flutter
    path('create_report_mobile/', create_report_mobile, name='create_report_mobile'),
    path('edit_report_mobile/', edit_report_mobile, name='edit_report_mobile'),
    path('delete_report_mobile/', delete_report_mobile, name='delete_report_mobile'),
    path('get_reports_mobile/', get_reports_mobile, name='get_reports_mobile'),
]

