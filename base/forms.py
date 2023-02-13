from django.db import models
from django_countries.fields import CountryField
from django import forms
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('ST','Stripe'),
    ('PP','Paypal')
)

class Checkoutform(forms.Form):
    f_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    l_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St',
        'class':'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Apartment',
        'class':'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-control'
    }))
    state = CountryField(blank_label='(State/Province)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-control'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
class PriceRange(forms.Form):
    min_price = forms.IntegerField(widget=forms.TextInput(attrs={
        'type':'number',
        'max':'5000',
        'min':'00',
        'step': '5',
        'class':'filter-min form-control-sm border flex-grow-1 text-muted border-0'
    }))
    max_price = forms.IntegerField(widget=forms.TextInput(attrs={
        'type':'number',
        'max':'5000',
        'min':'00',
        'step': '5',
        'class':'filter-max form-control-sm flex-grow-1 text-muted border-0'
    }))