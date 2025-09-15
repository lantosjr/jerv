from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser model
    """
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'company_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Egyéb információk', {
            'fields': ('phone_number', 'company_name')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Egyéb információk', {
            'fields': ('phone_number', 'company_name')
        }),
    )


# Register Group model for role management
# admin.site.register(Group)  # Already registered by Django