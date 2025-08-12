from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Review title'}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review...'}
            )
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError('Rating must be between 1 and 5')
        return rating
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise forms.ValidationError('Review title must be at least 5 characters long')
        return title.strip()
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 20:
            raise forms.ValidationError('Review content must be at least 20 characters long')
        return content.strip() 