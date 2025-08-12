from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('search/', views.movie_search, name='movie_search'),
    path('top-rated/', views.top_rated_movies, name='top_rated'),
    path('popular/', views.popular_movies, name='popular'),
    path('nepali/', views.nepali_movies, name='nepali_movies'),
] 