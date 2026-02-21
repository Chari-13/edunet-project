from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Alert


class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'disaster_type',
        'location',
        'colored_severity',
        'status',
        'latitude',
        'longitude',
        'date_time'
    )

    list_filter = ('status', 'severity', 'date_time')
    search_fields = ('disaster_type', 'location', 'description')
    readonly_fields = ('date_time',)

    fieldsets = (
        ('Alert Information', {
            'fields': ('disaster_type', 'location', 'severity')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Status & Time', {
            'fields': ('status', 'date_time')
        }),
    )

    def colored_severity(self, obj):
        color = "green"
        if obj.severity == "High":
            color = "red"
        elif obj.severity == "Medium":
            color = "orange"

        return format_html(
            '<span style="color:white; background:{}; padding:4px 8px; border-radius:5px;">{}</span>',
            color,
            obj.severity
        )

    colored_severity.short_description = "Severity"


# ✅ Register models ONLY ONCE
admin.site.register(UserProfile)
admin.site.register(Alert, AlertAdmin)

# ✅ Admin branding
admin.site.site_header = "🚨 Disaster Alert Admin Panel"
admin.site.site_title = "Disaster Admin"
admin.site.index_title = "Alert Management Dashboard"
