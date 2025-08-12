from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('sci-fi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('documentary', 'Documentary'),
        ('animation', 'Animation'),
        ('adventure', 'Adventure'),
    ]
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('nepali', 'Nepali'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('german', 'German'),
        ('chinese', 'Chinese'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
    ]
    
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    duration = models.IntegerField(help_text="Duration in minutes")
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    poster_url = models.URLField(blank=True, null=True, help_text="External URL for movie poster")
    trailer_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    director = models.CharField(max_length=200, blank=True, null=True)
    cast = models.TextField(blank=True, null=True, help_text="Comma-separated list of main cast")
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date']
    
    def __str__(self):
        return self.title
    
    @property
    def duration_formatted(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    
    @property
    def poster_display_url(self):
        """Return the poster URL, prioritizing uploaded file over external URL"""
        if self.poster:
            return self.poster.url
        elif self.poster_url:
            return self.poster_url
        return None
    
    @property
    def average_rating(self):
        """Calculate average rating from user reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0.0

    def get_cast_list(self):
        if not self.cast:
            return []
        return [name.strip() for name in self.cast.split(',') if name.strip()]

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['movie', 'user']  # One review per user per movie
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.movie.title}"
    
    @property
    def stars(self):
        """Return star rating as HTML"""
        full_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return full_stars + empty_stars
