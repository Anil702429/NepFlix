from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('pages:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def dashboard(request):
    """User dashboard with booking history and quick actions"""
    # Get user's recent bookings
    recent_bookings = request.user.bookings.all()[:5]
    
    # Get upcoming bookings
    from django.utils import timezone
    from booking.models import Booking
    
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        showtime__date__gte=timezone.now().date()
    ).order_by('showtime__date', 'showtime__time')[:5]
    
    context = {
        'recent_bookings': recent_bookings,
        'upcoming_bookings': upcoming_bookings,
    }
    
    return render(request, 'accounts/dashboard.html', context)
