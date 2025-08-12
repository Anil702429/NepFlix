from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'date_of_birth']
    list_filter = ['city', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city')
        }),
        ('Media', {
            'fields': ('profile_picture',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
