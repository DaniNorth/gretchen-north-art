from django import forms
from .models import CustomerProfile

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