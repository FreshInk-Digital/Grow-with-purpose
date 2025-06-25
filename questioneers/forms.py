from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inquiry


# sign up form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'aria-label': 'Email',
    }))
    
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'aria-label': 'Username',
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'aria-label': 'Password',
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'aria-label': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# inquiry form
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ['user', 'submitted_at']
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control', 'required': True})
            for field in Inquiry._meta.get_fields()
            if field.name not in ['id', 'user', 'submitted_at']
        }