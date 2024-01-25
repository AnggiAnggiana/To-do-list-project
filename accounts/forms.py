from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        labels = {
            'username': '',
            'email': '',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Type Your Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Type Your Password Again'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Type Password Again'})
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''