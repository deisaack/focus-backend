from django.contrib import admin
from .models import File, Approval

class ApprovalInline(admin.TabularInline):
    fieldsets = (
        (
            None,
            {
                'fields': ('user',)
            }
        ),
    )

    model = Approval
    extra = 0


class FileAdmin(admin.ModelAdmin):
    inlines = (ApprovalInline,)
    list_display = ['detail', 'user', 'item', 'created', ]
    list_filter = ['user',]

admin.site.register(File, FileAdmin)
admin.site.register(Approval)

