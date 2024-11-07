from django.urls import path
from .views import teacher_dashboard

app_name = 'teacher'


urlpatterns = [
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),
]
