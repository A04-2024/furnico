from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('create_report/<str:id>/', create_report_ajax, name='create_report'),
    path('admin_list_report_furniture/<str:id>/', admin_list_report_furniture, name='admin_list_report_furniture'),
    path('admin_list_report/', admin_list_report, name='admin_list_report'),
    path('delete_report/<int:id>/', delete_report, name='delete_report'),
    path('my_reports/', user_list_reports, name='user_list_reports'),
    
    # AJAX Endpoints
    path('get_report_data/<int:report_id>/', get_report_data, name='get_report_data'),
    path('edit_report_ajax/', edit_report_ajax, name='edit_report_ajax'),
    path('delete_report_ajax/<int:report_id>/', delete_report_ajax, name='delete_report_ajax'),
]

