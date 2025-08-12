from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'duration', 'rating', 'release_date', 'is_active')
    list_filter = ('genre', 'language', 'is_active', 'release_date')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    date_hierarchy = 'release_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'genre', 'language', 'duration', 'rating')
        }),
        ('Media', {
            'fields': ('poster', 'trailer_url')
        }),
        ('Release Information', {
            'fields': ('release_date', 'is_active')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at', 'movie__genre')
    search_fields = ('user__username', 'movie__title', 'title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'movie', 'rating', 'title', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')
