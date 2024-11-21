
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, StudentProfileView,
    StudentClassView,
    StudentSubjectView,
    StudentAttendanceHistoryView,
    StudentGradesView
)


app_name = 'student'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', StudentProfileView.as_view(), name='profile'),
    path('class/', StudentClassView.as_view(), name='student_class'),
    path('subjects/', StudentSubjectView.as_view(), name='student_subjects'),
    path('attendance/', StudentAttendanceHistoryView.as_view(),
         name='student_attendance_history'),
    path('grades/', StudentGradesView.as_view(), name='student_grades'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
