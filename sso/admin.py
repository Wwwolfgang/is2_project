from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Opcionales',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'descripcion',
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)