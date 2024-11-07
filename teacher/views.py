from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html', {'role': 'Teacher'})
