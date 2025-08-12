from django import forms
from .models import UserMembership

class MembershipCancellationForm(forms.Form):
    reason = forms.ChoiceField(
        choices=[
            ('too_expensive', 'Too expensive'),
            ('not_using', 'Not using enough'),
            ('switching', 'Switching to another service'),
            ('technical_issues', 'Technical issues'),
            ('other', 'Other'),
        ],
        widget=forms.RadioSelect,
        label='Why are you cancelling?'
    )
    
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us more about your experience...'}),
        required=False,
        label='Additional feedback'
    )
    
    keep_account = forms.BooleanField(
        initial=True,
        required=False,
        label='Keep my account active (I can reactivate anytime)'
    ) 