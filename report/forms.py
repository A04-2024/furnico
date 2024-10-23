from django import forms
from report.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'additional_info', 'report_image']  # Kolom yang diizinkan dalam form