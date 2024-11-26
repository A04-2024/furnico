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
    if request.method == 'POST' and request.is_ajax():
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.product_id = id  
            report.user = request.user
            report.save()
            return JsonResponse({'success': True})
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