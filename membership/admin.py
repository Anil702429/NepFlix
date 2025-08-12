from django.contrib import admin
from .models import MembershipTier, UserMembership, PaymentHistory

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_screens', 'max_quality', 'is_active', 'created_at']
    list_filter = ['is_active', 'name', 'max_quality']
    search_fields = ['name', 'description']
    ordering = ['price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'price', 'description', 'is_active')
        }),
        ('Features', {
            'fields': ('features', 'max_screens', 'max_quality')
        }),
    )

@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'tier', 'auto_renew', 'start_date']
    search_fields = ['user__username', 'user__email', 'stripe_subscription_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'tier')
        }),
        ('Subscription Details', {
            'fields': ('status', 'start_date', 'end_date', 'auto_renew')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'stripe_subscription_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership', 'amount', 'status', 'payment_date', 'payment_method']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['user__username', 'stripe_payment_id', 'description']
    readonly_fields = ['payment_date']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'membership', 'amount', 'currency', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'stripe_payment_id', 'description')
        }),
        ('Timestamps', {
            'fields': ('payment_date',),
            'classes': ('collapse',)
        }),
    )
