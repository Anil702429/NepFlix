from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from .models import Movie, Review
from .forms import ReviewForm
from booking.models import Booking

# Create your views here.

def movie_list(request):
    """Display Netflix-style movie list with categories - Nepali movies only"""
    # Featured movie (most recent or highest rated Nepali movie)
    featured_movie = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-release_date').first()
    
    # Trending Nepali movies (most booked in recent days)
    trending_movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        booking_count=Count('showtimes__bookings'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-booking_count', '-avg_rating')[:10]
    
    # Top rated Nepali movies
    top_rated_movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating', '-review_count')[:10]
    
    # Continue watching (for authenticated users) - Nepali movies only
    continue_watching = []
    if request.user.is_authenticated:
        # Get user's recent bookings and simulate watch progress
        recent_bookings = Booking.objects.filter(
            user=request.user,
            booking_status='confirmed',
            showtime__movie__language='nepali'
        ).select_related('showtime__movie').order_by('-booking_date')[:5]
        
        for booking in recent_bookings:
            # Simulate watch progress (random for demo)
            import random
            progress = random.randint(20, 80)
            continue_watching.append({
                'movie': booking.showtime.movie,
                'progress': progress
            })
    
    # All Nepali movies for the main grid
    movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-release_date')
    
    context = {
        'featured_movie': featured_movie,
        'trending_movies': trending_movies,
        'top_rated_movies': top_rated_movies,
        'continue_watching': continue_watching,
        'movies': movies,
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    """Display movie details and reviews"""
    movie = get_object_or_404(Movie, id=movie_id, is_active=True)
    reviews = movie.reviews.select_related('user').order_by('-created_at')
    
    # Check if user has already reviewed this movie
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    # Get user's booking history for this movie
    user_bookings = None
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(
            user=request.user,
            showtime__movie=movie
        ).select_related('showtime__theater')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = reviews.filter(rating=i).count()
    
    # Similar movies (same genre, excluding current movie)
    similar_movies = Movie.objects.filter(
        is_active=True,
        genre=movie.genre
    ).exclude(id=movie.id).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-avg_rating', '-release_date')[:6]
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'user_review': user_review,
        'user_bookings': user_bookings,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
        'similar_movies': similar_movies,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
def add_review(request, movie_id):
    """Add or update a review for a movie"""
    movie = get_object_or_404(Movie, id=movie_id, is_active=True)
    
    # Check if user has already reviewed this movie
    existing_review = Review.objects.filter(user=request.user, movie=movie).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            
            messages.success(request, 'Your review has been saved successfully!')
            return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'movie': movie,
        'existing_review': existing_review,
    }
    return render(request, 'movies/add_review.html', context)

@login_required
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_id = review.movie.id
    review.delete()
    messages.success(request, 'Your review has been deleted successfully!')
    return redirect('movies:movie_detail', movie_id=movie_id)

def movie_search(request):
    """Search Nepali movies by title, genre, or language"""
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    
    movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__icontains=query)
        )
    if genre:
        movies = movies.filter(genre=genre)
    
    # Get unique genres for filter dropdowns (Nepali movies only)
    genres = Movie.objects.filter(language='nepali').values_list('genre', flat=True).distinct()
    
    context = {
        'movies': movies,
        'query': query,
        'selected_genre': genre,
        'genres': genres,
    }
    return render(request, 'movies/movie_search.html', context)

def top_rated_movies(request):
    """Display top rated Nepali movies"""
    movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating', '-review_count')
    
    context = {
        'movies': movies,
        'title': 'Top Rated Nepali Movies'
    }
    return render(request, 'movies/movie_list.html', context)

def popular_movies(request):
    """Display most popular Nepali movies based on booking count"""
    movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        booking_count=Count('showtimes__bookings'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-booking_count', '-avg_rating')
    
    context = {
        'movies': movies,
        'title': 'Popular Nepali Movies'
    }
    return render(request, 'movies/movie_list.html', context)

def nepali_movies(request):
    """Display Nepali movies"""
    movies = Movie.objects.filter(
        is_active=True,
        language='nepali'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-release_date')
    
    context = {
        'movies': movies,
        'title': 'Nepali Movies',
        'is_nepali_section': True
    }
    return render(request, 'movies/movie_list.html', context)
