from django import forms
from .models import CustomerProfile, Wishlist

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'full_name',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'phone'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'e.g. Holiday Picks'}),
        }