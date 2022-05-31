
from django import forms
from .models import BillignsAddress

class BillignsAddressForm(forms.ModelForm):
    class Meta:
        model = BillignsAddress
        fields = ['address','zipcode','city','country','phone']