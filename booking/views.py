from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from .models import Booking, Payment, ShowTime, Seat
from .forms import CancellationForm
from django.conf import settings

@login_required
def user_bookings(request):
    """Display user's booking history and available movies in theaters"""
    from django.utils import timezone
    from datetime import date
    
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime__movie', 'showtime__theater'
    ).order_by('-booking_date')
    
    # Get available movies in theaters (showtimes for today and future dates)
    today = date.today()
    available_showtimes = ShowTime.objects.filter(
        date__gte=today,
        is_active=True
    ).select_related('movie', 'theater').order_by('date', 'time')
    
    # Group showtimes by movie for better display
    available_movies = {}
    total_showtimes = 0
    unique_theaters = set()
    earliest_date = None
    
    for showtime in available_showtimes:
        movie_key = showtime.movie.id
        if movie_key not in available_movies:
            available_movies[movie_key] = {
                'movie': showtime.movie,
                'showtimes': []
            }
        available_movies[movie_key]['showtimes'].append(showtime)
        total_showtimes += 1
        unique_theaters.add(showtime.theater.name)
        
        if earliest_date is None or showtime.date < earliest_date:
            earliest_date = showtime.date
    
    # Calculate booking statistics
    total_amount = sum(booking.total_amount for booking in bookings)
    confirmed_bookings = sum(1 for booking in bookings if booking.booking_status == 'confirmed')
    cancelled_bookings = sum(1 for booking in bookings if booking.booking_status == 'cancelled')
    
    context = {
        'bookings': bookings,
        'available_movies': available_movies,
        'total_showtimes': total_showtimes,
        'unique_theaters_count': len(unique_theaters),
        'earliest_date': earliest_date,
        'total_amount': total_amount,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings
    }
    return render(request, 'booking/user_bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    """Display detailed booking information"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking
    }
    return render(request, 'booking/booking_detail.html', context)

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking and process refund"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if booking can be cancelled
    if not booking.can_cancel:
        messages.error(request, 'This booking cannot be cancelled. Cancellation is only allowed up to 24 hours before the showtime.')
        return redirect('booking:booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = CancellationForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            try:
                with transaction.atomic():
                    # Update booking status
                    booking.booking_status = 'cancelled'
                    booking.cancelled_at = timezone.now()
                    booking.cancellation_reason = reason
                    booking.save()
                    
                    # Calculate refund amount
                    refund_percentage = booking.refund_percentage
                    refund_amount = (booking.total_amount * refund_percentage) / 100
                    booking.refund_amount = refund_amount
                    booking.refund_date = timezone.now()
                    booking.save()
                    
                    # Update payment status
                    if hasattr(booking, 'payment'):
                        payment = booking.payment
                        if refund_percentage == 100:
                            payment.payment_status = 'refunded'
                        else:
                            payment.payment_status = 'partially_refunded'
                        payment.refund_amount = refund_amount
                        payment.refund_date = timezone.now()
                        payment.save()
                    
                    # Free up seats
                    for seat in booking.seats.all():
                        seat.is_booked = False
                        seat.booking = None
                        seat.save()
                    
                    messages.success(
                        request, 
                        f'Booking cancelled successfully! Refund amount: रु {refund_amount:.2f} ({refund_percentage}% of total)'
                    )
                    return redirect('booking:user_bookings')
                    
            except Exception as e:
                messages.error(request, f'Error cancelling booking: {str(e)}')
                return redirect('booking:booking_detail', booking_id=booking.id)
    else:
        form = CancellationForm()
    
    context = {
        'booking': booking,
        'form': form,
        'refund_percentage': booking.refund_percentage,
        'refund_amount': (booking.total_amount * booking.refund_percentage) / 100
    }
    return render(request, 'booking/cancel_booking.html', context)

@login_required
def select_seats(request, showtime_id):
    """Select seats for a showtime"""
    showtime = get_object_or_404(ShowTime, id=showtime_id, is_active=True)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        if not selected_seats:
            messages.error(request, 'Please select at least one seat.')
            return redirect('booking:select_seats', showtime_id=showtime_id)
        
        # Calculate total amount
        total_amount = len(selected_seats) * showtime.price
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            total_amount=total_amount,
            payment_status='pending'
        )
        
        # Assign seats to booking
        for seat_id in selected_seats:
            seat = Seat.objects.get(id=seat_id, showtime=showtime, is_booked=False)
            seat.is_booked = True
            seat.booking = booking
            seat.save()
        
        return redirect('booking:checkout', booking_id=booking.id)
    
    # Get all seats for this showtime
    seats = Seat.objects.filter(showtime=showtime).order_by('row', 'seat_number')
    
    # Group seats by row
    seat_rows = {}
    for seat in seats:
        if seat.row not in seat_rows:
            seat_rows[seat.row] = []
        seat_rows[seat.row].append(seat)
    
    context = {
        'showtime': showtime,
        'seat_rows': seat_rows,
        'total_price': showtime.price
    }
    return render(request, 'booking/select_seats.html', context)

@login_required
def checkout(request, booking_id):
    """Checkout page for payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if booking is already paid
    if booking.payment_status == 'completed':
        messages.warning(request, 'This booking has already been paid for.')
        return redirect('booking:booking_detail', booking_id=booking.id)
    
    context = {
        'booking': booking,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY if hasattr(settings, 'STRIPE_PUBLISHABLE_KEY') else 'pk_test_your_key_here'
    }
    return render(request, 'booking/checkout.html', context)

@login_required
def process_payment(request, booking_id):
    """Process payment form submission"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Get payment method and details from form
            payment_method = request.POST.get('payment_method')
            stripe_token = request.POST.get('stripeToken')
            
            # Validate payment method
            if not payment_method:
                messages.error(request, 'Please select a payment method.')
                return redirect('booking:checkout', booking_id=booking.id)
            
            # Process based on payment method
            if payment_method == 'credit_card':
                # Validate card payment details
                cardholder_name = request.POST.get('cardholder_name')
                billing_email = request.POST.get('billing_email')
                billing_address = request.POST.get('billing_address')
                billing_city = request.POST.get('billing_city')
                billing_state = request.POST.get('billing_state')
                billing_zip = request.POST.get('billing_zip')
                billing_country = request.POST.get('billing_country')
                
                if not all([stripe_token, cardholder_name, billing_email, billing_address, 
                           billing_city, billing_state, billing_zip, billing_country]):
                    messages.error(request, 'Please fill in all required payment details.')
                    return redirect('booking:checkout', booking_id=booking.id)
                
                # Here you would typically process the payment with Stripe
                # For now, we'll simulate a successful payment
                payment_method_display = 'Stripe'
                
            elif payment_method in ['khalti', 'esewa']:
                # Validate digital wallet details
                mobile_number = request.POST.get('mobile_number')
                
                if not mobile_number or len(mobile_number) != 10:
                    messages.error(request, 'Please enter a valid mobile number.')
                    return redirect('booking:checkout', booking_id=booking.id)
                
                # Here you would integrate with Khalti/eSewa APIs
                # For now, we'll simulate a successful payment
                payment_method_display = 'Khalti' if payment_method == 'khalti' else 'eSewa'
                
            elif payment_method == 'cash':
                # Cash payment - no additional validation needed
                payment_verification = request.POST.get('payment_verification', '')
                payment_method_display = 'Cash at Counter'
                
            else:
                messages.error(request, 'Invalid payment method selected.')
                return redirect('booking:checkout', booking_id=booking.id)
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_amount,
                payment_method=payment_method,
                payment_status='completed',
                transaction_id=f'TXN_{booking.booking_id.hex[:8].upper()}'
            )
            
            # Update booking payment status
            booking.payment_status = 'completed'
            booking.save()
            
            # Show appropriate success message based on payment method
            if payment_method == 'cash':
                messages.success(request, f'Booking confirmed! Please pay रु {booking.total_amount} at the theater counter before the showtime.')
            else:
                messages.success(request, f'Payment completed successfully via {payment_method_display}! Your booking is confirmed.')
            
            return redirect('booking:booking_detail', booking_id=booking.id)
            
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
            return redirect('booking:checkout', booking_id=booking.id)
    
    return redirect('booking:checkout', booking_id=booking.id)
