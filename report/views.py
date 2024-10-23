from django.shortcuts import render, redirect, get_object_or_404
from .models import Furniture, Report
from report.forms import ReportForm  # Asumsikan kamu punya form ReportForm

# View untuk membuat laporan
def create_report(request, furniture_id):
    furniture = get_object_or_404(Furniture, pk=furniture_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.furniture = furniture
            report.user = request.user
            report.save()
            return redirect('furniture_detail', furniture_id=furniture_id)
    else:
        form = ReportForm()
    
    return render(request, 'report/create_report.html', {'form': form, 'furniture': furniture})

# View untuk melihat daftar laporan (untuk admin)
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report/report_list.html', {'reports': reports})