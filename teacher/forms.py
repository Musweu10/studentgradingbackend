# teacher/forms.py
from django import forms
from .models import Grade, Class,Subject
from accounts.models import User


class GradeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Grade
        fields = ['student', 'mid_term_score', 'final_exam_score']
        widgets = {
            'mid_term_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_exam_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'teacher', 'students']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'class_assigned', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_assigned': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }
