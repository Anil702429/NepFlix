from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from movies.models import Movie
from booking.models import Booking

# Create your views here.

def home(request):
    """Home page view with featured Nepali movies and statistics"""
    # Get featured Nepali movies (latest 6 movies)
    featured_movies = Movie.objects.filter(language='nepali').order_by('-release_date')[:6]
    
    # Get some statistics for the homepage
    total_movies = Movie.objects.filter(language='nepali').count()
    total_bookings = Booking.objects.filter(showtime__movie__language='nepali').count()
    
    # If no Nepali movies exist, create some dummy data for demonstration
    if not featured_movies.exists():
        featured_movies = [
            {
                'title': 'Loot',
                'genre': 'Comedy',
                'rating': 4,
                'poster': None
            },
            {
                'title': 'Kabaddi',
                'genre': 'Drama',
                'rating': 5,
                'poster': None
            },
            {
                'title': 'Pashupati Prasad',
                'genre': 'Drama',
                'rating': 5,
                'poster': None
            }
        ]
    
    context = {
        'featured_movies': featured_movies,
        'total_movies': total_movies,
        'total_bookings': total_bookings,
    }
    return render(request, 'pages/home.html', context)

def about(request):
    """About us page view"""
    context = {
        'team_members': [
            {
                'name': 'John Smith',
                'position': 'CEO & Founder',
                'bio': 'Passionate about bringing the best movie experience to our customers.',
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
                'social': {
                    'linkedin': '#',
                    'twitter': '#',
                    'email': 'john@nepflix.com'
                }
            },
            {
                'name': 'Sarah Johnson',
                'position': 'Head of Operations',
                'bio': 'Ensuring smooth operations and excellent customer service.',
                'image': None,
                'social': {
                    'linkedin': '#',
                    'twitter': '#',
                    'email': 'sarah@nepflix.com'
                }
            },
            {
                'name': 'Mike Chen',
                'position': 'Lead Developer',
                'bio': 'Building amazing digital experiences for movie lovers.',
                'image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
                'social': {
                    'linkedin': '#',
                    'twitter': '#',
                    'email': 'mike@nepflix.com'
                }
            },
            {
                'name': 'Emily Davis',
                'position': 'Marketing Director',
                'bio': 'Creating compelling campaigns to connect with our audience.',
                'image': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
                'social': {
                    'linkedin': '#',
                    'twitter': '#',
                    'email': 'emily@nepflix.com'
                }
            }
        ],
        'stats': [
            {'number': '50K+', 'label': 'Happy Customers'},
            {'number': '15+', 'label': 'Nepali Movies Available'},
            {'number': '24/7', 'label': 'Customer Support'},
            {'number': '99%', 'label': 'Satisfaction Rate'}
        ]
    }
    return render(request, 'pages/about.html', context)

def contact(request):
    """Contact us page view with contact form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # Send email (you'll need to configure email settings)
                send_mail(
                    f'Contact Form: {subject}',
                    f'From: {name}\nEmail: {email}\n\nMessage:\n{message}',
                    email,
                    [settings.DEFAULT_FROM_EMAIL] if hasattr(settings, 'DEFAULT_FROM_EMAIL') else ['admin@nepflix.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {
        'contact_info': {
            'address': '123 Movie Street, Cinema City, CC 12345',
            'phone': '+1 (555) 123-4567',
            'email': 'info@nepflix.com',
            'hours': 'Monday - Sunday: 9:00 AM - 11:00 PM'
        }
    }
    return render(request, 'pages/contact.html', context)
