from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from authentication.models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):

    inlines = [
    ]

    add_fieldsets = AuthUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'first_name', 'last_name',),
        }),
    )

    list_display = [
        'email',
        'full_name',
        'is_staff',
        'is_superuser',
        'is_active',
        'last_login',
        'date_joined',
    ]

    list_filter = [
        'is_staff',
        'is_active',
        'is_superuser',
        'last_login',
        'date_joined'
    ]

    ordering = (
        '-date_joined',
        'username',
    )

    search_fields = [
        'email',
        'first_name',
        'last_name',
    ]

    readonly_fields = [
        'date_joined'
    ]

    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related(
    #         'socialaccount_set',
    #     )
