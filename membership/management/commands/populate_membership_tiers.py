from django.core.management.base import BaseCommand
from membership.models import MembershipTier

class Command(BaseCommand):
    help = 'Populate membership tiers with sample data'

    def handle(self, *args, **options):
        # Clear existing tiers
        MembershipTier.objects.all().delete()
        
        # Create Basic tier
        basic_tier = MembershipTier.objects.create(
            name='basic',
            price=999.00,
            description='Good video quality in a single mobile, tablet, computer, or TV screen.',
            features=[
                'Watch on 1 screen at a time',
                'SD (Standard Definition) quality',
                'Download on 1 device'
            ],
            max_screens=1,
            max_quality='SD',
            stripe_price_id='price_basic_test'  # Placeholder for testing
        )
        
        # Create Standard tier
        standard_tier = MembershipTier.objects.create(
            name='standard',
            price=1499.00,
            description='Better video quality in two screens. Watch in HD.',
            features=[
                'Watch on 2 screens at a time',
                'HD (High Definition) quality',
                'Download on 2 devices'
            ],
            max_screens=2,
            max_quality='HD',
            stripe_price_id='price_standard_test'  # Placeholder for testing
        )
        
        # Create Premium tier
        premium_tier = MembershipTier.objects.create(
            name='premium',
            price=1999.00,
            description='Best video quality in four screens. Watch in Ultra HD.',
            features=[
                'Watch on 4 screens at a time',
                'Ultra HD (4K) quality',
                'Download on 4 devices'
            ],
            max_screens=4,
            max_quality='UHD',
            stripe_price_id='price_premium_test'  # Placeholder for testing
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created 3 membership tiers:\n'
                f'- Basic: रु {basic_tier.price}/month\n'
                f'- Standard: रु {standard_tier.price}/month\n'
                f'- Premium: रु {premium_tier.price}/month\n\n'
                f'Note: Stripe price IDs are set to placeholder values. Update them with real Stripe price IDs for production.'
            )
        ) 