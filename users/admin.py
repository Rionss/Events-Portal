from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name', 'first_name', 'last_name', 'phone')
    list_filter = ('department', 'batch', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'department', 'batch', 'phone', 'thumbnail')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'first_name', 'last_name', 'department', 'batch', 'phone', 'thumbnail', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )

admin.site.register(User, UserAdminConfig)