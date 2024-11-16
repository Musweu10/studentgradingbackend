# # teacher/urls.py
# from . import views
# from django.urls import path
#
# app_name = 'teacher'
#
#
# urlpatterns = [
#     path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
#     path('add-class/', views.add_class, name='add_class'),
#     path('add-subject/', views.add_subject, name='add_subject'),
#     #     path('class/<uuid:class_id>/manage/',
#     #          views.manage_class, name='manage_class'),
#     path('class/<uuid:class_id>/subject/<uuid:subject_id>/add-grade/',
#          views.add_grade, name='add_grade'),
#     path('class/<uuid:class_id>/mark-attendance/',
#          views.mark_attendance, name='mark_attendance'),
#     path('manage-class/<int:class_id>/',
#          views.manage_class, name='manage_class'),
# ]


# teacher/urls.py

from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-class/', views.add_class, name='add_class'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('manage-class/<uuid:class_id>/',
         views.manage_class, name='manage_class'),
    path('class/<uuid:class_id>/subject/<uuid:subject_id>/add-grade/',
         views.add_grade, name='add_grade'),
    path('class/<uuid:class_id>/mark-attendance/',
         views.mark_attendance, name='mark_attendance'),
    path('class/<uuid:class_id>/view-grades/',
         views.view_grades, name='view_grades'),
    path('class/<uuid:class_id>/student/<uuid:student_id>/view-grades/',
         views.view_student_grades, name='view_student_grades'),
    path('class/<uuid:class_id>/attendance-history/',
         views.view_attendance_history, name='view_attendance_history'),
]
