from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from theaters.models import Theater
import uuid

class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['movie', 'theater', 'date', 'time']
    
    def __str__(self):
        return f"{self.movie.title} - {self.theater.name} - {self.date} {self.time}"

class Seat(models.Model):
    ROW_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
        ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'),
        ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'),
    ]
    
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1, choices=ROW_CHOICES)
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='seats')
    
    class Meta:
        unique_together = ['showtime', 'row', 'seat_number']
        ordering = ['row', 'seat_number']
    
    def __str__(self):
        return f"{self.row}{self.seat_number} - {self.showtime}"
    
    @property
    def seat_label(self):
        return f"{self.row}{self.seat_number}"

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    BOOKING_STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='bookings')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"
    
    @property
    def seat_count(self):
        return self.seats.count()
    
    @property
    def movie_title(self):
        return self.showtime.movie.title
    
    @property
    def theater_name(self):
        return self.showtime.theater.name
    
    @property
    def can_cancel(self):
        """Check if booking can be cancelled (within 24 hours of showtime)"""
        from django.utils import timezone
        from datetime import timedelta
        
        show_datetime = timezone.make_aware(
            timezone.datetime.combine(self.showtime.date, self.showtime.time)
        )
        current_time = timezone.now()
        
        # Can cancel if more than 24 hours before showtime
        return (show_datetime - current_time) > timedelta(hours=24)
    
    @property
    def refund_percentage(self):
        """Calculate refund percentage based on cancellation time"""
        from django.utils import timezone
        from datetime import timedelta
        
        show_datetime = timezone.make_aware(
            timezone.datetime.combine(self.showtime.date, self.showtime.time)
        )
        current_time = timezone.now()
        time_diff = show_datetime - current_time
        
        if time_diff > timedelta(hours=24):
            return 100  # Full refund
        elif time_diff > timedelta(hours=2):
            return 50   # 50% refund
        else:
            return 0    # No refund

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit/Debit Card'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('cash', 'Cash at Counter'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment for {self.booking} - {self.amount}"
