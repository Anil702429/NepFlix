from django.contrib import admin
from .models import ShowTime, Seat, Booking, Payment

@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'date', 'time', 'price', 'is_active')
    list_filter = ('is_active', 'date', 'theater')
    search_fields = ('movie__title', 'theater__name')
    date_hierarchy = 'date'
    list_editable = ('is_active', 'price')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'row', 'seat_number', 'is_booked', 'booking')
    list_filter = ('is_booked', 'row', 'showtime__movie', 'showtime__theater')
    search_fields = ('showtime__movie__title', 'showtime__theater__name')
    list_editable = ('is_booked',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'movie_title', 'theater_name', 'total_amount', 
                   'booking_status', 'payment_status', 'booking_date')
    list_filter = ('booking_status', 'payment_status', 'booking_date', 'showtime__theater')
    search_fields = ('booking_id', 'user__username', 'showtime__movie__title', 'showtime__theater__name')
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_id', 'booking_date', 'updated_at')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'showtime', 'total_amount', 'booking_status')
        }),
        ('Payment Information', {
            'fields': ('payment_status',)
        }),
        ('Cancellation Information', {
            'fields': ('cancelled_at', 'cancellation_reason', 'refund_amount', 'refund_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('booking_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def movie_title(self, obj):
        return obj.movie_title
    movie_title.short_description = 'Movie'
    
    def theater_name(self, obj):
        return obj.theater_name
    theater_name.short_description = 'Theater'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'showtime__movie', 'showtime__theater'
        )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_method', 'payment_status', 'payment_date')
    search_fields = ('booking__booking_id', 'transaction_id')
    date_hierarchy = 'payment_date'
    readonly_fields = ('payment_date', 'updated_at')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('booking', 'amount', 'payment_method', 'payment_status', 'transaction_id')
        }),
        ('Refund Information', {
            'fields': ('refund_amount', 'refund_date', 'refund_transaction_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
