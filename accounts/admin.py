from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "username")
    fieldsets = UserAdmin.fieldsets + (
        ("Custom user fields", {"fields": ("bio", "photo")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
