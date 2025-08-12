from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from movies.models import Movie, Review
from booking.models import Booking, Payment, ShowTime
from accounts.models import UserProfile
from theaters.models import Theater

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with comprehensive analytics"""
    
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    # Basic statistics
    total_movies = Movie.objects.count()
    total_users = UserProfile.objects.count()
    total_theaters = Theater.objects.count()
    total_bookings = Booking.objects.count()
    
    # Revenue statistics
    total_revenue = Payment.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_revenue = Payment.objects.filter(
        payment_status='completed',
        payment_date__gte=last_30_days
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    weekly_revenue = Payment.objects.filter(
        payment_status='completed',
        payment_date__gte=last_7_days
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Booking statistics
    recent_bookings = Booking.objects.filter(
        booking_date__gte=last_7_days
    ).count()
    
    cancelled_bookings = Booking.objects.filter(
        booking_status='cancelled'
    ).count()
    
    # Movie statistics
    top_movies = Movie.objects.annotate(
        booking_count=Count('showtimes__bookings')
    ).order_by('-booking_count')[:5]
    
    top_rated_movies = Movie.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
    
    # User statistics
    active_users = UserProfile.objects.filter(
        user__bookings__booking_date__gte=last_30_days
    ).distinct().count()
    
    # Recent activity
    recent_bookings_list = Booking.objects.select_related(
        'user', 'showtime__movie', 'showtime__theater'
    ).order_by('-booking_date')[:10]
    
    recent_reviews = Review.objects.select_related(
        'user', 'movie'
    ).order_by('-created_at')[:10]
    
    # Chart data for revenue
    daily_revenue = []
    for i in range(7):
        date = today - timedelta(days=i)
        revenue = Payment.objects.filter(
            payment_status='completed',
            payment_date__date=date
        ).aggregate(total=Sum('amount'))['total'] or 0
        daily_revenue.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(revenue)
        })
    daily_revenue.reverse()
    
    # Genre popularity
    genre_stats = Movie.objects.values('genre').annotate(
        count=Count('id'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-count')
    
    # Payment method statistics
    payment_methods = Payment.objects.values('payment_method').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    ).order_by('-total_amount')
    
    context = {
        'total_movies': total_movies,
        'total_users': total_users,
        'total_theaters': total_theaters,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'weekly_revenue': weekly_revenue,
        'recent_bookings': recent_bookings,
        'cancelled_bookings': cancelled_bookings,
        'top_movies': top_movies,
        'top_rated_movies': top_rated_movies,
        'active_users': active_users,
        'recent_bookings_list': recent_bookings_list,
        'recent_reviews': recent_reviews,
        'daily_revenue': daily_revenue,
        'genre_stats': genre_stats,
        'payment_methods': payment_methods,
        'last_30_days': last_30_days,
        'last_7_days': last_7_days,
    }
    
    return render(request, 'analytics/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def booking_analytics(request):
    """Detailed booking analytics"""
    
    # Date filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    bookings = Booking.objects.select_related(
        'user', 'showtime__movie', 'showtime__theater'
    )
    
    if start_date:
        bookings = bookings.filter(booking_date__date__gte=start_date)
    if end_date:
        bookings = bookings.filter(booking_date__date__lte=end_date)
    
    # Booking trends
    booking_trends = bookings.extra(
        select={'date': 'date(booking_date)'}
    ).values('date').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('date')
    
    # Movie performance
    movie_performance = bookings.values(
        'showtime__movie__title'
    ).annotate(
        booking_count=Count('id'),
        total_revenue=Sum('total_amount'),
        avg_rating=Avg('showtime__movie__reviews__rating')
    ).order_by('-total_revenue')
    
    # Theater performance
    theater_performance = bookings.values(
        'showtime__theater__name'
    ).annotate(
        booking_count=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('-total_revenue')
    
    context = {
        'booking_trends': booking_trends,
        'movie_performance': movie_performance,
        'theater_performance': theater_performance,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'analytics/booking_analytics.html', context)

@login_required
@user_passes_test(is_admin)
def user_analytics(request):
    """User behavior analytics"""
    
    # User registration trends
    registration_trends = UserProfile.objects.extra(
        select={'date': 'date(created_at)'}
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # User activity
    active_users = UserProfile.objects.filter(
        user__bookings__booking_date__gte=timezone.now() - timedelta(days=30)
    ).distinct().count()
    
    total_users = UserProfile.objects.count()
    user_activity_rate = (active_users / total_users * 100) if total_users > 0 else 0
    
    # Top users by bookings
    top_users = UserProfile.objects.annotate(
        booking_count=Count('user__bookings'),
        total_spent=Sum('user__bookings__total_amount')
    ).order_by('-total_spent')[:10]
    
    # User demographics
    user_cities = UserProfile.objects.values('city').annotate(
        count=Count('id')
    ).exclude(city__isnull=True).exclude(city='').order_by('-count')
    
    context = {
        'registration_trends': registration_trends,
        'active_users': active_users,
        'total_users': total_users,
        'user_activity_rate': user_activity_rate,
        'top_users': top_users,
        'user_cities': user_cities,
    }
    
    return render(request, 'analytics/user_analytics.html', context)
