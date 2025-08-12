# NepFlix Membership System

A Netflix-style membership system for the NepFlix movie booking platform.

## Features

### Membership Tiers
- **Basic Plan** (रु 999/month): SD quality, 1 screen
- **Standard Plan** (रु 1,499/month): HD quality, 2 screens  
- **Premium Plan** (रु 1,999/month): Ultra HD quality, 4 screens

### Key Features
- ✅ Netflix-style pricing and UI
- ✅ Stripe payment integration
- ✅ Subscription management
- ✅ Payment history tracking
- ✅ Cancel/reactivate functionality
- ✅ Responsive design
- ✅ Admin interface

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Stripe
Update your Stripe keys in `nepflix/settings.py`:
```python
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_stripe_publishable_key'
STRIPE_SECRET_KEY = 'sk_test_your_stripe_secret_key'
STRIPE_WEBHOOK_SECRET = 'whsec_your_stripe_webhook_secret'
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Populate Sample Data
```bash
python manage.py populate_membership_tiers
```

### 5. Create Stripe Products
In your Stripe dashboard, create products for each tier:
- Basic: रु 999/month
- Standard: रु 1,499/month  
- Premium: रु 1,999/month

### 6. Update Database
Add the Stripe price IDs to your membership tiers in Django admin or via management command.

## Usage

### For Users
1. Visit `/membership/plans/` to see available plans
2. Choose a plan and click "Start [Plan Name]"
3. Complete payment with Stripe
4. Manage subscription at `/membership/my-membership/`

### For Admins
- Manage tiers in Django admin at `/admin/membership/`
- View subscription analytics
- Monitor payment history

## URLs

- `/membership/plans/` - View membership plans
- `/membership/subscribe/<tier_id>/` - Subscribe to a plan
- `/membership/my-membership/` - Manage current membership
- `/membership/cancel/` - Cancel membership
- `/membership/reactivate/` - Reactivate cancelled membership
- `/membership/webhook/stripe/` - Stripe webhook endpoint

## Models

### MembershipTier
- `name`: Basic, Standard, Premium
- `price`: Monthly price
- `description`: Plan description
- `features`: JSON list of features
- `max_screens`: Number of simultaneous screens
- `max_quality`: Video quality (SD, HD, Ultra HD)

### UserMembership
- `user`: OneToOne relationship with User
- `tier`: ForeignKey to MembershipTier
- `status`: Active, Cancelled, Expired, Pending
- `start_date`: When subscription started
- `end_date`: When subscription ends
- `auto_renew`: Boolean for auto-renewal
- `stripe_subscription_id`: Stripe subscription ID

### PaymentHistory
- `user`: ForeignKey to User
- `membership`: ForeignKey to UserMembership
- `amount`: Payment amount
- `status`: Payment status
- `payment_method`: Payment method used
- `stripe_payment_id`: Stripe payment ID

## Customization

### Adding New Tiers
1. Create new tier in Django admin
2. Add corresponding Stripe product
3. Update the plans template if needed

### Modifying Features
Edit the `features` JSON field in MembershipTier model or update the management command.

### Styling
The membership pages use custom CSS that can be modified in the template files:
- `templates/membership/plans.html`
- `templates/membership/subscribe.html`
- `templates/membership/my_membership.html`

## Security Notes

- All payments are processed through Stripe
- No credit card data is stored locally
- Webhook verification ensures payment integrity
- CSRF protection on all forms

## Testing

Test the membership system with Stripe test cards:
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- Requires authentication: 4000 0025 0000 3155

## Troubleshooting

### Common Issues
1. **Stripe keys not working**: Ensure you're using test keys for development
2. **Webhook not receiving events**: Check webhook endpoint URL in Stripe dashboard
3. **Payment failing**: Verify Stripe product/price IDs are correct

### Debug Mode
Set `DEBUG = True` in settings to see detailed error messages.

## Future Enhancements

- [ ] Free trial period
- [ ] Annual billing options
- [ ] Family plans
- [ ] Gift subscriptions
- [ ] Referral program
- [ ] Usage analytics
- [ ] Email notifications
- [ ] Mobile app integration 