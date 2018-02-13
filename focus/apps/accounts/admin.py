from __future__ import absolute_import
from django.contrib import admin
from . models import Employee, User
from django.contrib.auth.models import Group


class EmployeeInline(admin.TabularInline):
        fieldsets = (
            (
                None,
                {
                    'fields': ('employee_no', 'phone_verified', 'gender')
                }
            ),
        )

        model = Employee
        extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = (EmployeeInline,)
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_active',]
    list_filter = ['is_active', 'is_staff' ]

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Employee)
