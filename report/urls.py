from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('admin_list_report_furniture/<str:id>/', admin_list_report_furniture, name='admin_list_report_furniture'),
    path('admin_list_report/', admin_list_report, name='admin_list_report'),
    path('delete_report/<int:id>/', delete_report, name='delete_report'),
    path('my_reports/', user_list_reports, name='user_list_reports'),
    path('get_filtered_reports_json/', get_filtered_reports_json, name='get_filtered_reports_json'),
    path('get_report_data/<int:report_id>/', get_report_data, name='get_report_data'),


    # AJAX Endpoints
    path('create_report/<str:id>/', create_report_ajax, name='create_report'),
    path('edit_report_ajax/', edit_report_ajax, name='edit_report_ajax'),
    path('delete_report_ajax/<int:report_id>/', delete_report_ajax, name='delete_report_ajax'),


    path('create_report/<int:id>/', create_report_ajax_mobile, name='create_report_ajax'),
    path('update_report/<int:report_id>/', update_report_ajax, name='update_report_ajax'),
    path('delete_report/<int:report_id>/', delete_report_ajax, name='delete_report_ajax'),
    path('get_reports/', get_reports_ajax, name='get_reports_ajax'),
]

