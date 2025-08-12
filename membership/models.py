from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class MembershipTier(models.Model):
    TIER_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=50, choices=TIER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    features = models.JSONField(default=list)  # List of features for this tier
    max_screens = models.IntegerField(default=1)
    max_quality = models.CharField(max_length=20, default='HD')
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)  # Added Stripe price ID
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.get_name_display()} - रु {self.price}/month"
    
    @property
    def display_price(self):
        return f"रु {self.price}/month"

class UserMembership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    tier = models.ForeignKey(MembershipTier, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tier.name}"
    
    def is_active(self):
        if self.status == 'active':
            if self.end_date and self.end_date < timezone.now():
                self.status = 'expired'
                self.save()
                return False
            return True
        return False
    
    def cancel_membership(self):
        self.status = 'cancelled'
        self.auto_renew = False
        self.save()
    
    def renew_membership(self):
        self.status = 'active'
        self.auto_renew = True
        if self.end_date:
            self.end_date = self.end_date + timedelta(days=30)
        else:
            self.end_date = timezone.now() + timedelta(days=30)
        self.save()

class PaymentHistory(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('cash', 'Cash at Counter'),
        ('stripe', 'Stripe'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NPR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True, null=True)  # For additional payment information
    
    def __str__(self):
        return f"{self.user.username} - रु {self.amount} - {self.status}"
    
    class Meta:
        ordering = ['-payment_date']
