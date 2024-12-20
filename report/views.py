from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from editp.models import UserProfile
from show_products.models import Product
from report.forms import ReportForm
from report.models import Report
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from uuid import UUID
from django.contrib.auth.models import User # UserDummy


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
def get_filtered_reports_json(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        furniture_id = request.GET.get('furniture_id')
        user_id = request.GET.get('user_id')
        reports = Report.objects.all()
        if furniture_id:
            reports = reports.filter(furniture_id=furniture_id)
        if user_id:
            reports = reports.filter(user_id=user_id)

        data = [
            {
                'id': report.id,
                'user': report.user.username,
                'furniture': report.furniture.name,
                'reason': report.reason,
                'additional_info': report.additional_info,
                'date_reported': report.date_reported.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for report in reports
        ]
        return JsonResponse({'success': True, 'reports': data}, safe=False)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


# ==============================================
# FLUTTERRR 
# ==============================================
@csrf_exempt
def create_report_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user')
        furniture_id = data.get('furniture')
        reason = data.get('reason')
        additional_info = data.get('additional_info', '')
        
        try:
            user = User.objects.get(id=user_id)
            report = Report.objects.create(
                user=user,
                furniture_id=furniture_id,
                reason=reason,
                additional_info=additional_info
            )
            return JsonResponse({"status": "success", "report_id": report.id}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User tidak ditemukan."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error"}, status=401)
@csrf_exempt
def get_reports_mobile(request):
    if request.method == 'GET':
        reports = Report.objects.select_related('furniture', 'user').all()
        reports_list = []
        for report in reports:
            reports_list.append({
                "id": report.id,
                "user_id": report.user.id,
                "username": report.user.username, 
                "furniture_id": report.furniture.id,
                "furniture_name": report.furniture.product_name,
                "reason": report.reason,
                "additional_info": report.additional_info,
                "date_reported": report.date_reported.isoformat(),
            })
        return JsonResponse(reports_list, safe=False)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)
@csrf_exempt
def delete_report_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report_id = data.get('report_id')
            report = Report.objects.get(id=report_id)
            report.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Report.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Report not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_report_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report_id = data.get('report_id')
            reason = data.get('reason')
            additional_info = data.get('additional_info', '')

            report = Report.objects.get(id=report_id)
            report.reason = reason
            report.additional_info = additional_info
            report.save()

            return JsonResponse({"status": "success"}, status=200)
        except Report.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Report not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=401)