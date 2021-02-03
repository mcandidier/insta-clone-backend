from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, ResetPassword


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Basic Information', {
            'fields': ('username', 'profile_photo', 'first_name', 'last_name')}
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),

    )
    search_fields = ('email',)
    ordering = ('email',)


class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ['email', 'token', 'date_created']
    # readonly_fields = ['token', 'date_created']

admin.site.register(User, UserAdmin)
admin.site.register(ResetPassword, ResetPasswordAdmin)