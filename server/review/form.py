from django import forms
from .models import Review, Store

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_score', 'review_content', 'phone_number',)
        widgets = {
            'review_content': forms.Textarea(
                attrs={'class': 'review-area', 'placeholder': 'Write review to help us better', 'required': 'True'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'review-input', 'placeholder': 'Phone number (optional)', 'required': 'True'}),
            'review_score': forms.HiddenInput(
                attrs={'id': 'id_review_score1'}),
        }
        labels = {
            'review_content': '',
            'phone_number': ''
        }

class ReviewFormGoogle(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_score',)
        widgets = {
            'review_score': forms.HiddenInput(
                attrs={'id': 'id_review_score2'}),
        }