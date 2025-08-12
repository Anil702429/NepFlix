# Khalti Payment Integration Setup Guide

## Overview
This guide explains how to set up Khalti payment integration for the NepFlix membership system.

## Prerequisites
1. A Khalti merchant account
2. Valid Khalti API credentials (Public Key and Secret Key)

## Step 1: Get Khalti API Credentials

### For Production:
1. Sign up for a Khalti merchant account at [https://khalti.com/](https://khalti.com/)
2. Complete the merchant verification process
3. Get your API credentials from the Khalti merchant dashboard

### For Testing:
1. Use Khalti's test environment
2. Get test API credentials from Khalti's developer documentation

## Step 2: Configure Django Settings

Update your `nepflix/settings.py` file with your Khalti credentials:

```python
# Khalti Payment Settings
KHALTI_PUBLIC_KEY = 'your_actual_public_key_here'  # Replace with your real public key
KHALTI_SECRET_KEY = 'your_actual_secret_key_here'  # Replace with your real secret key
KHALTI_VERIFY_URL = 'https://khalti.com/api/v2/payment/verify/'
KHALTI_INITIATE_URL = 'https://khalti.com/api/v2/epayment/initiate/'
KHALTI_RETURN_URL = 'https://yourdomain.com/membership/khalti-return/{membership_id}/'
```

## Step 3: Environment Variables (Recommended)

For security, use environment variables instead of hardcoding credentials:

1. Create a `.env` file in your project root:
```env
KHALTI_PUBLIC_KEY=your_actual_public_key_here
KHALTI_SECRET_KEY=your_actual_secret_key_here
```

2. Update your settings.py to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Khalti Payment Settings
KHALTI_PUBLIC_KEY = os.getenv('KHALTI_PUBLIC_KEY', 'test_public_key_1234567890abcdef')
KHALTI_SECRET_KEY = os.getenv('KHALTI_SECRET_KEY', 'test_secret_key_1234567890abcdef')
```

## Step 4: Test the Integration

1. Start your Django development server
2. Navigate to a membership subscription page
3. Select "Khalti Digital Wallet" as payment method
4. Fill in the required details and submit

## Error Handling

### Common Issues:

1. **401 - Invalid Token Error**
   - Check that your KHALTI_SECRET_KEY is correct
   - Ensure you're using the right environment (test vs production)

2. **400 - Validation Error**
   - Check that your KHALTI_PUBLIC_KEY is correct
   - Verify the payment amount format

3. **Connection Timeout**
   - Check your internet connection
   - Verify Khalti API endpoints are accessible

## Development Mode

When `DEBUG = True` in your Django settings, the system will:
- Show a warning message about using test mode
- Simulate successful payments for testing
- Allow you to test the payment flow without real API calls

## Production Deployment

For production:
1. Set `DEBUG = False`
2. Use real Khalti API credentials
3. Update `KHALTI_RETURN_URL` to your production domain
4. Test thoroughly with small amounts first

## Security Notes

- Never commit API credentials to version control
- Use environment variables for sensitive data
- Regularly rotate your API keys
- Monitor payment logs for suspicious activity

## Support

If you encounter issues:
1. Check Khalti's official documentation
2. Verify your API credentials
3. Test with Khalti's sandbox environment first
4. Contact Khalti support for API-related issues 