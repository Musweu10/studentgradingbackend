# accounts/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from teacher.admin import GradeInline
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'role', 'phone_number', 'date_joined', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active')
    ordering = ('-date_joined',)

    # Optionally customize the display of the role or any other fields
    def role(self, obj):
        return format_html('<span style="color: blue;">{}</span>', obj.role)


admin.site.register(User, UserAdmin)

# Register your models here.

# Assuming User is the Student model


# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'role')
#     list_filter = ('role',)
#     search_fields = ('first_name', 'last_name', 'email')
#
#     inlines = [GradeInline]  # Add the Grade inline to the Student Admin
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Optionally, filter students by their role if necessary
#         # Ensure only students are shown
#         return queryset.filter(role='student')
