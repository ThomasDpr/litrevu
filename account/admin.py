from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('email',)}),)


admin.site.register(CustomUser, CustomUserAdmin)
