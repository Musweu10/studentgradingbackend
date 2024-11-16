from django.urls import path
from .views import RegisterView, LoginView, LogoutView, StudentProfileView, StudentAttendanceView

app_name = 'student'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', StudentProfileView.as_view(), name='profile'),
    path('attendance/', StudentAttendanceView.as_view(), name='attendance_history'),
]
