from django.contrib import admin
from .models import Theater

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'email', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['name', 'address', 'city']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'city')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
