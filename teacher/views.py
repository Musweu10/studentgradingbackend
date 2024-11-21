from django.shortcuts import render, redirect, get_object_or_404

from config import settings
from .models import Class, Subject, Attendance, Grade
from accounts.models import User
from .models import Class, Subject, Attendance
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GradeForm, AddClassForm, AddSubjectForm
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
# Create your views here.
from django.shortcuts import render
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('core:index')  # Redirect if not a teacher

    teacher = request.user
    classes = Class.objects.filter(teacher=teacher)
    # Fetch all subjects assigned to the teacher
    subjects = Subject.objects.filter(teacher=request.user)
    # Calculate total students count across all classes
    total_students = sum(cls.students.count() for cls in classes)
    # Log the classes for debugging
    logger.debug(f"Classes for {teacher.get_full_name()}: {classes}")
    ctx = {
        'user': request.user,
        'role': request.user.role,
        'classes': classes,
        'subjects': subjects,
        'total_students': total_students,

    }
    return render(request, 'teacher/dashboard.html', ctx)


@login_required
def add_grade(request, class_id, subject_id):
    if request.user.role != 'teacher':
        return redirect('index')  # Only teachers should access this view

    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    subject = get_object_or_404(
        Subject, id=subject_id, class_assigned=class_obj)
    students = class_obj.students.all()

    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.subject = subject
            grade.save()
            return redirect('teacher:manage_class', class_id=class_id)
    else:
        form = GradeForm()

    return render(request, 'teacher/add_grade.html', {
        'class': class_obj,
        'subject': subject,
        'students': students,
        'form': form
    })


@login_required
def manage_class(request, class_id):
    if request.user.role != 'teacher':
        return redirect('index')

    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    students = class_obj.students.all()
    subjects = Subject.objects.filter(class_assigned=class_obj)
    return render(request, 'teacher/manage_class.html', {'class': class_obj, 'students': students, 'subjects': subjects})


# @login_required
# def mark_attendance(request, class_id):
#     if request.user.role != 'teacher':
#         return redirect('index')
#
#     class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
#     if request.method == "POST":
#         for student_id, is_present in request.POST.items():
#             if student_id.startswith('student_'):
#                 student = get_object_or_404(
#                     User, id=student_id.replace('student_', ''))
#                 Attendance.objects.update_or_create(
#                     class_assigned=class_obj,
#                     student=student,
#                     date=timezone.now(),
#                     defaults={'is_present': is_present == 'on'}
#                 )
#         return redirect('teacher:teacher_dashboard')
#     students = class_obj.students.all()
#     context = {
#         'class': class_obj,
#         'students': students,
#     }
#     return render(request, 'teacher/mark_attendance.html', context)

@login_required
def mark_attendance(request, class_id):
    if request.user.role != 'teacher':
        return redirect('index')

    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)

    if request.method == "POST":
        attendance_date = request.POST.get('date')
        if attendance_date:
            attendance_date = timezone.datetime.strptime(
                attendance_date, '%Y-%m-%d').date()

        for student_id, is_present in request.POST.items():
            if student_id.startswith('student_'):
                student = get_object_or_404(
                    User, id=student_id.replace('student_', ''))
                Attendance.objects.update_or_create(
                    class_assigned=class_obj,
                    student=student,
                    date=attendance_date,  # Use the selected date
                    defaults={'is_present': is_present == 'on'}
                )
        return redirect('teacher:teacher_dashboard')

    students = class_obj.students.all()
    context = {
        'class': class_obj,
        'students': students,
    }
    return render(request, 'teacher/mark_attendance.html', context)


@login_required
def add_class(request):
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the teacher's dashboard after saving
            return redirect('teacher:dashboard')
    else:
        form = AddClassForm()

    context = {
        'form': form,
    }
    return render(request, 'teacher/add_class.html', context)


@login_required
def add_subject(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect back to the teacher's dashboard
            return redirect('teacher:teacher_dashboard')
    else:
        form = AddSubjectForm()

    context = {
        'form': form,
    }
    return render(request, 'teacher/add_subject.html', context)


@login_required
def view_grades(request, class_id):
    if request.user.role != 'teacher':
        return redirect('index')

    # Fetch the class object and verify that the logged-in teacher is assigned to this class
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)

    # Get all subjects assigned to this class
    subjects = Subject.objects.filter(class_assigned=class_obj)

    # Fetch all grades for the students in this class
    grades = Grade.objects.filter(subject__in=subjects)

    # Get unique students from the grades
    students = {grade.student for grade in grades}

    context = {
        'class_obj': class_obj,
        'students': students,
    }
    return render(request, 'teacher/view_grades.html', context)


@login_required
def view_student_grades(request, class_id, student_id):
    # Verify if the logged-in user is a teacher
    if request.user.role != 'teacher':
        return redirect('index')

    # Fetch the class object and ensure the teacher is assigned to the class
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)

    # Fetch the student object by ID and role
    student = get_object_or_404(
        get_user_model(), id=student_id, role='student')

    # Fetch grades for the student in the selected class
    grades = Grade.objects.filter(
        student=student, subject__class_assigned=class_obj)

    context = {
        'class_obj': class_obj,
        'student': student,
        'grades': grades,
    }
    return render(request, 'teacher/view_student_grades.html', context)


@login_required
def view_attendance_history(request, class_id):
    if request.user.role != 'teacher':
        return redirect('index')

    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)

    # Default filter range to the current day
    filter_range = request.GET.get('filter_range', 'day')
    today = timezone.now().date()
    start_date = today

    # Determine the date range based on the filter
    if filter_range == 'day':
        start_date = today
    elif filter_range == 'week':
        start_date = today - timedelta(days=7)
    elif filter_range == 'month':
        start_date = today - timedelta(days=30)
    elif filter_range == 'term':  # Assuming a term is 3 months
        start_date = today - timedelta(days=90)

    # Initialize the attendance records safely
    attendance_records = Attendance.objects.filter(
        class_assigned=class_obj,
        date__range=[start_date, today]
    ).order_by('-date')

    # Calculate the percentage of students present
    total_records = attendance_records.count()
    present_records = attendance_records.filter(is_present=True).count()
    attendance_percentage = (
        present_records / total_records * 100) if total_records > 0 else 0

    context = {
        'class': class_obj,
        'filter_range': filter_range,
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'teacher/view_attendance_history.html', context)
