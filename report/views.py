from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from editp.models import UserProfile
from show_products.models import Product
from report.forms import ReportForm
from report.models import Report
from django.http import JsonResponse

@login_required
def create_report_ajax(request, id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.furniture = get_object_or_404(Product, id=id)
            report.user = request.user
            report.save()
            return JsonResponse({'success': True, 'report_id': report.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



@login_required
def admin_list_report_furniture(request, id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'admin':
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('show_products:show_main')  

    furniture = get_object_or_404(Product, id=id)
    reports = Report.objects.filter(furniture=furniture)
    report_count = Report.objects.filter(product_id=id).count()

    return render(request, 'admin_list_report.html', {
        'reports': reports,
        'furniture': furniture,
        'count': report_count
    })

@login_required
def admin_list_report(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'admin':
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('show_products:show_main')  

    reports = Report.objects.all()
    report_count = Report.objects.count()

    return render(request, 'admin_list_report.html', {
        'reports': reports,
        'count': report_count
    })

@login_required
def get_report_data(request, report_id):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        report = get_object_or_404(Report, id=report_id, user=request.user)
        data = {
            'success': True,
            'reason': report.reason,
            'additional_info': report.additional_info,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def edit_report_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        report_id = request.POST.get('report_id')
        report = get_object_or_404(Report, id=report_id, user=request.user)
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.user != report.user and user_profile.role != 'admin':
        messages.error(request, "Anda tidak memiliki izin untuk menghapus laporan ini.")
        return redirect('report:user_list_reports')

    if request.method == 'POST':
        report.delete()
        messages.success(request, "Laporan berhasil dihapus.")
        return redirect('report:user_list_reports')
    return render(request, 'confirm_delete_report.html', {'report': report})

@login_required
def delete_report_ajax(request, report_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        report = get_object_or_404(Report, id=report_id)
        # Check if the user is the report owner or an admin
        if request.user == report.user or request.user.userprofile.role == 'admin':
            report.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Permission denied.'}, status=403)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    
@login_required
def user_list_reports(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'user_list_reports.html', {'reports': reports})
