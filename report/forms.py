from django import forms
from report.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'additional_info']
        widgets = {
            'reason': forms.RadioSelect(),
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }
