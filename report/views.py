from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from editp.models import UserProfile
from show_products.models import Product
from report.forms import ReportForm
from report.models import Report
from django.http import JsonResponse

# @login_required
def create_report_ajax(request, product_id):
    furniture = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.furniture = furniture
            report.save()
            return JsonResponse({'message': 'Terima Kasih Atas Laporan Anda'})
    else:
        form = ReportForm()

    return render(request, 'create_report.html', {'form': form})

# @login_required
def admin_jumlah_report_ajax(request, product_id):
    # user_profile = get_object_or_404(UserProfile, user=request.user)
    # if user_profile.tipe != 'admin':
    #     messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
    #     return redirect('show_products:show_main')  # Atau halaman lain untuk non-admin


    furniture = get_object_or_404(Product, id=product_id)
    report_count = Report.objects.filter(furniture=furniture).count()

    return render(request, 'admin_jumlah_report_ajax.html', {
        'furniture': furniture,
        'report_count': report_count
    })

# @login_required
def admin_list_report_furniture(request, product_id):
    # user_profile = get_object_or_404(UserProfile, user=request.user)
    # if user_profile.tipe != 'admin':
    #     messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
    #     return redirect('show_products:show_main')  # Atau halaman lain untuk non-admin

    furniture = get_object_or_404(Product, id=product_id)
    reports = Report.objects.filter(furniture=furniture)

    return render(request, 'admin_list_report.html', {
        'reports': reports,
        'furniture': furniture
    })

# @login_required
def admin_list_report(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.role != 'admin':
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('show_products:show_main')  # Atau halaman lain untuk non-admin

    reports = Report.objects.all()

    return render(request, 'admin_list_report.html', {'reports': reports})