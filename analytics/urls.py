from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('booking/', views.booking_analytics, name='booking_analytics'),
    path('users/', views.user_analytics, name='user_analytics'),
] 