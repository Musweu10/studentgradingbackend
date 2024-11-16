from django.contrib import admin
from .models import Class, Subject, Attendance, Grade
# Inline admin for Grades


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0  # No extra empty forms
    fields = ('subject', 'mid_term_score', 'final_exam_score', 'total_score')
    readonly_fields = ('subject', 'mid_term_score',
                       'final_exam_score', 'total_score')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')
    filter_horizontal = ('students',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'class_assigned')
    list_filter = ('teacher', 'class_assigned')
    search_fields = ('name', 'teacher__first_name',
                     'teacher__last_name', 'class_assigned__name')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_assigned', 'date', 'is_present')
    list_filter = ('class_assigned', 'date')
    search_fields = ('student__first_name',
                     'student__last_name', 'class_assigned__name')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'mid_term_score',
                    'final_exam_score', 'total_score')
    list_filter = ('subject',)
    search_fields = ('student__first_name',
                     'student__last_name', 'subject__name')

    # Optional: Remove list_display_links to avoid showing links to grades
    list_display_links = None
