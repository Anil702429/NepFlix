from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from django.conf import settings
import json
from django.urls import reverse

from .models import MembershipTier, UserMembership, PaymentHistory
from .services import KhaltiPaymentService

# Initialize Khalti
khalti_service = KhaltiPaymentService()

def membership_plans(request):
    """Display membership plans/tiers like Netflix"""
    tiers = MembershipTier.objects.filter(is_active=True).order_by('price')
    
    # Check if user already has a membership
    user_membership = None
    if request.user.is_authenticated:
        try:
            user_membership = request.user.membership
        except UserMembership.DoesNotExist:
            pass
    
    context = {
        'tiers': tiers,
        'user_membership': user_membership,
    }
    return render(request, 'membership/plans.html', context)

@login_required
def subscribe(request, tier_id):
    """Subscribe to a membership tier"""
    tier = get_object_or_404(MembershipTier, id=tier_id, is_active=True)
    
    # Check if user already has an active membership
    try:
        existing_membership = request.user.membership
        if existing_membership.is_active():
            messages.warning(request, 'You already have an active membership.')
            return redirect('membership:my_membership')
    except UserMembership.DoesNotExist:
        pass
    
    if request.method == 'POST':
        try:
            # Parse JSON data from frontend
            data = json.loads(request.body)
            payment_method = data.get('payment_method', 'khalti')
            
            # Handle different payment methods
            if payment_method == 'khalti':
                return handle_khalti_payment(request, tier, data)
            elif payment_method == 'khalti_dummy':
                return handle_khalti_dummy_payment(request, tier, data)
            elif payment_method == 'esewa':
                return handle_esewa_payment(request, tier, data)
            elif payment_method == 'cash':
                return handle_cash_payment(request, tier, data)
            else:
                return JsonResponse({'error': 'Invalid payment method'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    context = {
        'tier': tier,
    }
    return render(request, 'membership/subscribe.html', context)



def handle_khalti_payment(request, tier, data):
    """Handle Khalti payment"""
    try:
        mobile_number = data.get('mobile_number')
        full_name = data.get('full_name')
        
        if not mobile_number or not full_name:
            return JsonResponse({'error': 'Mobile number and full name are required'}, status=400)
        
        # Create membership with pending status
        with transaction.atomic():
            membership = UserMembership.objects.create(
                user=request.user,
                tier=tier,
                status='pending',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30)
            )
            
            # Create payment history record
            PaymentHistory.objects.create(
                user=request.user,
                membership=membership,
                amount=tier.price,
                payment_method='khalti',
                status='pending',
                transaction_id=f'KHALTI_{membership.id}_{int(timezone.now().timestamp())}'
            )
        
        # Initiate Khalti payment using the service
        return_url = request.build_absolute_uri(
            reverse('membership:khalti_return', kwargs={'membership_id': membership.id})
        )
        
        payment_result = khalti_service.initiate_payment(
            amount=tier.price,
            user=request.user,
            membership_tier=tier,
            return_url=return_url
        )
        
        if payment_result['success']:
            # Create payment record with Khalti idx
            khalti_service.create_payment_record(
                user=request.user,
                membership=membership,
                amount=tier.price,
                khalti_idx=payment_result['idx']
            )
            
            return JsonResponse({
                'success': True,
                'redirect_url': payment_result['payment_url'],
                'message': 'Khalti payment initiated successfully'
            })
        else:
            # Handle Khalti API errors
            error_message = payment_result.get('error', 'Unknown error')

            # Development fallback for common credential/setup issues
            if settings.DEBUG and (
                '401' in error_message or
                'Invalid token' in error_message or
                'credentials not configured' in error_message.lower()
            ):
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('membership:my_membership'),
                    'message': 'Khalti payment simulated successfully (development mode)',
                    'warning': 'Using test mode - Khalti API credentials not configured'
                })

            # Production: surface the error
            return JsonResponse({
                'error': f'Khalti payment failed: {error_message}'
            }, status=400)
        
    except Exception as e:
        return JsonResponse({'error': f'Khalti payment failed: {str(e)}'}, status=500)

def handle_khalti_dummy_payment(request, tier, data):
    """Simulate a successful Khalti payment without external API calls"""
    try:
        mobile_number = data.get('mobile_number')
        full_name = data.get('full_name')

        if not mobile_number or not full_name:
            return JsonResponse({'error': 'Mobile number and full name are required'}, status=400)

        with transaction.atomic():
            membership = UserMembership.objects.create(
                user=request.user,
                tier=tier,
                status='active',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                payment_method='khalti'
            )

            PaymentHistory.objects.create(
                user=request.user,
                membership=membership,
                amount=tier.price,
                payment_method='khalti',
                status='completed',
                transaction_id=f'KHALTI_DUMMY_{membership.id}_{int(timezone.now().timestamp())}',
                description=f"Dummy Khalti payment for {tier.get_name_display()} membership"
            )

        return JsonResponse({
            'success': True,
            'redirect_url': reverse('membership:my_membership'),
            'message': 'Dummy Khalti payment successful (test mode)'
        })
    except Exception as e:
        return JsonResponse({'error': f'Dummy Khalti payment failed: {str(e)}'}, status=500)
def handle_esewa_payment(request, tier, data):
    """Handle eSewa payment"""
    try:
        mobile_number = data.get('mobile_number')
        full_name = data.get('full_name')
        
        if not mobile_number or not full_name:
            return JsonResponse({'error': 'Mobile number and full name are required'}, status=400)
        
        # Create membership with pending status
        with transaction.atomic():
            membership = UserMembership.objects.create(
                user=request.user,
                tier=tier,
                status='pending',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30)
            )
            
            # Create payment history record
            PaymentHistory.objects.create(
                user=request.user,
                membership=membership,
                amount=tier.price,
                payment_method='esewa',
                status='pending',
                transaction_id=f'ESEWA_{membership.id}_{int(timezone.now().timestamp())}'
            )
        
        # Here you would integrate with eSewa API
        # For now, we'll simulate a successful payment
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('membership:my_membership'),
            'message': 'eSewa payment initiated successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': f'eSewa payment failed: {str(e)}'}, status=500)

def handle_cash_payment(request, tier, data):
    """Handle cash payment"""
    try:
        theater_location = data.get('theater_location')
        
        if not theater_location:
            return JsonResponse({'error': 'Theater location is required'}, status=400)
        
        # Create membership with pending status
        with transaction.atomic():
            membership = UserMembership.objects.create(
                user=request.user,
                tier=tier,
                status='pending',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30)
            )
            
            # Create payment history record
            PaymentHistory.objects.create(
                user=request.user,
                membership=membership,
                amount=tier.price,
                payment_method='cash',
                status='pending',
                transaction_id=f'CASH_{membership.id}_{int(timezone.now().timestamp())}',
                notes=f'Payment to be made at: {theater_location}'
            )
        
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('membership:my_membership'),
            'message': f'Cash payment confirmed. Please visit {theater_location} to complete your payment.'
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Cash payment failed: {str(e)}'}, status=500)

@login_required
def test_subscribe(request, tier_id):
    """Test subscription without real Stripe integration"""
    tier = get_object_or_404(MembershipTier, id=tier_id, is_active=True)
    
    # Check if user already has an active membership
    try:
        existing_membership = request.user.membership
        if existing_membership.is_active():
            messages.warning(request, 'You already have an active membership.')
            return redirect('membership:my_membership')
    except UserMembership.DoesNotExist:
        pass
    
    if request.method == 'POST':
        try:
            # Create membership in database (simulate successful payment)
            with transaction.atomic():
                membership = UserMembership.objects.create(
                    user=request.user,
                    tier=tier,
                    status='active',  # Set as active for testing
                    payment_method='test'
                )
                
                # Create payment record
                PaymentHistory.objects.create(
                    user=request.user,
                    membership=membership,
                    amount=tier.price,
                    status='completed',
                    payment_method='test',
                    description=f"Test subscription to {tier.get_name_display()} plan"
                )
            
            messages.success(request, f'Successfully subscribed to {tier.get_name_display()} plan!')
            return redirect('membership:my_membership')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'tier': tier,
    }
    return render(request, 'membership/test_subscribe.html', context)

@login_required
def khalti_subscribe(request, tier_id):
    """Subscribe to a membership tier using Khalti payment"""
    tier = get_object_or_404(MembershipTier, id=tier_id, is_active=True)
    
    # Check if user already has an active membership
    try:
        existing_membership = request.user.membership
        if existing_membership.is_active():
            messages.warning(request, 'You already have an active membership.')
            return redirect('membership:my_membership')
    except UserMembership.DoesNotExist:
        pass
    
    if request.method == 'POST':
        try:
            # Create membership in database first
            with transaction.atomic():
                membership = UserMembership.objects.create(
                    user=request.user,
                    tier=tier,
                    status='pending',
                    payment_method='khalti'
                )
                
                # Initiate Khalti payment
                return_url = request.build_absolute_uri(
                    reverse('membership:khalti_return', kwargs={'membership_id': membership.id})
                )
                
                payment_result = khalti_service.initiate_payment(
                    amount=tier.price,
                    user=request.user,
                    membership_tier=tier,
                    return_url=return_url
                )
                
                if payment_result['success']:
                    # Create payment record
                    khalti_service.create_payment_record(
                        user=request.user,
                        membership=membership,
                        amount=tier.price,
                        khalti_idx=payment_result['idx']
                    )
                    
                    # Redirect to Khalti payment page
                    return redirect(payment_result['payment_url'])
                else:
                    # Payment initiation failed
                    membership.delete()
                    messages.error(request, f'Payment initiation failed: {payment_result["error"]}')
                    return redirect('membership:plans')
                    
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('membership:plans')
    
    context = {
        'tier': tier,
    }
    return render(request, 'membership/khalti_subscribe.html', context)

@login_required
def test_khalti_subscribe(request, tier_id):
    """Test Khalti subscription without real payment"""
    tier = get_object_or_404(MembershipTier, id=tier_id, is_active=True)
    
    # Check if user already has an active membership
    try:
        existing_membership = request.user.membership
        if existing_membership.is_active():
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': 'You already have an active membership.'
                })
            messages.warning(request, 'You already have an active membership.')
            return redirect('membership:my_membership')
    except UserMembership.DoesNotExist:
        pass
    
    if request.method == 'POST':
        try:
            # Check if this is an AJAX request
            if request.headers.get('Content-Type') == 'application/json':
                # Handle AJAX request for test payment
                data = json.loads(request.body)
                action = data.get('action')
                
                if action == 'test_payment':
                    # Create membership in database (simulate successful payment)
                    with transaction.atomic():
                        membership = UserMembership.objects.create(
                            user=request.user,
                            tier=tier,
                            status='active',  # Set as active for testing
                            payment_method='khalti'
                        )
                        
                        # Create payment record
                        PaymentHistory.objects.create(
                            user=request.user,
                            membership=membership,
                            amount=tier.price,
                            status='completed',
                            payment_method='khalti',
                            stripe_payment_id='test_khalti_payment_123',
                            description=f"Test Khalti payment for {tier.get_name_display()} plan"
                        )
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Successfully subscribed to {tier.get_name_display()} plan with Khalti!',
                        'amount': tier.price,
                        'redirect_url': reverse('membership:my_membership')
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid action'
                    })
            else:
                # Handle regular form submission (fallback)
                # Create membership in database (simulate successful payment)
                with transaction.atomic():
                    membership = UserMembership.objects.create(
                        user=request.user,
                        tier=tier,
                        status='active',  # Set as active for testing
                        payment_method='khalti'
                    )
                    
                    # Create payment record
                    PaymentHistory.objects.create(
                        user=request.user,
                        membership=membership,
                        amount=tier.price,
                        status='completed',
                        payment_method='khalti',
                        stripe_payment_id='test_khalti_payment_123',
                        description=f"Test Khalti payment for {tier.get_name_display()} plan"
                    )
                
                messages.success(request, f'Successfully subscribed to {tier.get_name_display()} plan with Khalti!')
                return redirect('membership:my_membership')
                
        except Exception as e:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': f'An error occurred: {str(e)}'
                })
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'tier': tier,
    }
    return render(request, 'membership/test_khalti_subscribe.html', context)

@login_required
def khalti_return(request, membership_id):
    """Handle Khalti payment return"""
    try:
        membership = UserMembership.objects.get(id=membership_id, user=request.user)
    except UserMembership.DoesNotExist:
        messages.error(request, 'Membership not found.')
        return redirect('membership:plans')
    
    # Get payment parameters from Khalti
    token = request.GET.get('token')
    amount = request.GET.get('amount')
    
    if not token or not amount:
        messages.error(request, 'Invalid payment response from Khalti.')
        membership.delete()  # Clean up failed membership
        return redirect('membership:plans')
    
    try:
        # Verify payment with Khalti
        verification_result = khalti_service.verify_payment(token, float(amount))
        
        if verification_result['success']:
            # Payment successful
            membership.status = 'active'
            membership.save()
            
            # Update payment record
            payment = PaymentHistory.objects.filter(
                membership=membership,
                payment_method='khalti'
            ).first()
            
            if payment:
                payment.status = 'completed'
                payment.save()
            
            messages.success(request, f'Successfully subscribed to {membership.tier.get_name_display()} plan!')
            return redirect('membership:my_membership')
        else:
            # Payment verification failed
            messages.error(request, f'Payment verification failed: {verification_result["error"]}')
            membership.delete()
            return redirect('membership:plans')
            
    except Exception as e:
        messages.error(request, f'Payment verification error: {str(e)}')
        membership.delete()
        return redirect('membership:plans')

@login_required
def my_membership(request):
    """Display user's current membership status"""
    try:
        membership = request.user.membership
    except UserMembership.DoesNotExist:
        membership = None
    
    # Get payment history
    payment_history = PaymentHistory.objects.filter(user=request.user).order_by('-payment_date')[:10]
    
    context = {
        'membership': membership,
        'payment_history': payment_history,
    }
    return render(request, 'membership/my_membership.html', context)

@login_required
def cancel_membership(request):
    """Cancel user's membership"""
    try:
        membership = request.user.membership
        if membership.is_active():
            # Cancel in Stripe
            if membership.stripe_subscription_id:
                stripe.Subscription.modify(
                    membership.stripe_subscription_id,
                    cancel_at_period_end=True
                )
            
            # Cancel in database
            membership.cancel_membership()
            messages.success(request, 'Your membership has been cancelled. You can continue using the service until the end of your billing period.')
        else:
            messages.warning(request, 'You don\'t have an active membership to cancel.')
    except UserMembership.DoesNotExist:
        messages.warning(request, 'You don\'t have a membership to cancel.')
    
    return redirect('membership:my_membership')

@login_required
def reactivate_membership(request):
    """Reactivate a cancelled membership"""
    try:
        membership = request.user.membership
        if membership.status == 'cancelled':
            # Reactivate in Stripe
            if membership.stripe_subscription_id:
                stripe.Subscription.modify(
                    membership.stripe_subscription_id,
                    cancel_at_period_end=False
                )
            
            # Reactivate in database
            membership.renew_membership()
            messages.success(request, 'Your membership has been reactivated!')
        else:
            messages.warning(request, 'Your membership is not cancelled.')
    except UserMembership.DoesNotExist:
        messages.warning(request, 'You don\'t have a membership to reactivate.')
    
    return redirect('membership:my_membership')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks for subscription updates"""
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        
        if event['type'] == 'invoice.payment_succeeded':
            subscription_id = event['data']['object']['subscription']
            try:
                membership = UserMembership.objects.get(stripe_subscription_id=subscription_id)
                membership.status = 'active'
                membership.save()
                
                # Update payment record
                payment = PaymentHistory.objects.filter(
                    membership=membership,
                    stripe_payment_id=event['data']['object']['payment_intent']
                ).first()
                if payment:
                    payment.status = 'completed'
                    payment.save()
                    
            except UserMembership.DoesNotExist:
                pass
                
        elif event['type'] == 'invoice.payment_failed':
            subscription_id = event['data']['object']['subscription']
            try:
                membership = UserMembership.objects.get(stripe_subscription_id=subscription_id)
                membership.status = 'pending'
                membership.save()
            except UserMembership.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
