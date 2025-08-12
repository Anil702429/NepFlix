from django import forms

class CancellationForm(forms.Form):
    REASON_CHOICES = [
        ('change_of_plans', 'Change of Plans'),
        ('emergency', 'Emergency'),
        ('found_better_seats', 'Found Better Seats'),
        ('movie_cancelled', 'Movie Cancelled'),
        ('technical_issue', 'Technical Issue'),
        ('other', 'Other'),
    ]
    
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Please select a reason for cancellation'
    )
    
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional notes (optional)'
        }),
        required=False,
        max_length=500
    )
    
    def clean_additional_notes(self):
        notes = self.cleaned_data.get('additional_notes')
        if notes and len(notes.strip()) > 500:
            raise forms.ValidationError('Additional notes cannot exceed 500 characters.')
        return notes.strip() if notes else '' 