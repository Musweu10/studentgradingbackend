# accounts/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'date_joined', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active')
    ordering = ('-date_joined',)

    # Optionally customize the display of the role or any other fields
    def role(self, obj):
        return format_html('<span style="color: blue;">{}</span>', obj.role)

# Register your custom user model
admin.site.register(User, UserAdmin)
