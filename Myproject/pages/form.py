from django import forms
from .models import PerformanceReview

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'knowledge_of_work',
            'quality_of_work',
            'productivity',
            'initiative',
            'communication_skills',
            'overall_performance',
            'comments'
        ]
        widgets = {
            'knowledge_of_work': forms.Select(attrs={'class': 'form-control'}),
            'quality_of_work': forms.Select(attrs={'class': 'form-control'}),
            'productivity': forms.Select(attrs={'class': 'form-control'}),
            'initiative': forms.Select(attrs={'class': 'form-control'}),
            'communication_skills': forms.Select(attrs={'class': 'form-control'}),
            'overall_performance': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
