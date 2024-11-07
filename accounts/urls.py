from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/teacher/', views.teacher_register, name='teacher_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
