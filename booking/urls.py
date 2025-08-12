from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('showtime/<int:showtime_id>/seats/', views.select_seats, name='select_seats'),
    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
] 