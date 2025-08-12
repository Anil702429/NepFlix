import requests
import json
from django.conf import settings
from django.utils import timezone
from .models import PaymentHistory

class KhaltiPaymentService:
    def __init__(self):
        self.public_key = settings.KHALTI_PUBLIC_KEY
        self.secret_key = settings.KHALTI_SECRET_KEY
        self.verify_url = settings.KHALTI_VERIFY_URL
        self.initiate_url = settings.KHALTI_INITIATE_URL
        self.return_url = settings.KHALTI_RETURN_URL
    
    def initiate_payment(self, amount, user, membership_tier, return_url=None):
        """
        Initiate Khalti payment
        """
        try:
            # Check if Khalti credentials are properly configured
            if not self.public_key or self.public_key == 'test_public_key_1234567890abcdef':
                return {
                    'success': False,
                    'error': 'Khalti API credentials not configured. Please set KHALTI_PUBLIC_KEY and KHALTI_SECRET_KEY in settings.'
                }
            
            if not self.secret_key or self.secret_key == 'test_secret_key_1234567890abcdef':
                return {
                    'success': False,
                    'error': 'Khalti API credentials not configured. Please set KHALTI_PUBLIC_KEY and KHALTI_SECRET_KEY in settings.'
                }
            
            payload = {
                "public_key": self.public_key,
                "amount": int(amount * 100),  # Convert to paisa (smallest unit)
                "product_identity": f"membership_{membership_tier.id}",
                "product_name": f"NepFlix {membership_tier.get_name_display()} Membership",
                "customer_info": {
                    "name": f"{user.first_name} {user.last_name}".strip() or user.username,
                    "email": user.email,
                    "phone": user.profile.phone if hasattr(user, 'profile') and hasattr(user.profile, 'phone') else ""
                },
                "return_url": return_url or self.return_url,
                "cancel_url": return_url or self.return_url,
            }
            
            headers = {
                "Authorization": f"Key {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.initiate_url,
                json=payload,
                headers=headers,
                timeout=30  # Add timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'payment_url': data.get('payment_url'),
                    'idx': data.get('idx'),
                    'data': data
                }
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': f'Khalti API authentication failed: Invalid API credentials. Please check your KHALTI_SECRET_KEY.'
                }
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    return {
                        'success': False,
                        'error': f'Khalti API validation error: {error_data.get("detail", response.text)}'
                    }
                except:
                    return {
                        'success': False,
                        'error': f'Khalti API validation error: {response.text}'
                    }
            else:
                return {
                    'success': False,
                    'error': f'Khalti API error: {response.status_code} - {response.text}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Khalti API request timed out. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Unable to connect to Khalti API. Please check your internet connection.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Payment initiation failed: {str(e)}'
            }
    
    def verify_payment(self, token, amount):
        """
        Verify Khalti payment
        """
        try:
            payload = {
                "token": token,
                "amount": int(amount * 100)  # Convert to paisa
            }
            
            headers = {
                "Authorization": f"Key {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.verify_url,
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'error': f'Payment verification failed: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Payment verification failed: {str(e)}'
            }
    
    def create_payment_record(self, user, membership, amount, khalti_idx, status='pending'):
        """
        Create payment record in database
        """
        return PaymentHistory.objects.create(
            user=user,
            membership=membership,
            amount=amount,
            status=status,
            payment_method='khalti',
            stripe_payment_id=khalti_idx,  # Using stripe_payment_id field for Khalti idx
            description=f"Khalti payment for {membership.tier.get_name_display()} membership"
        ) 