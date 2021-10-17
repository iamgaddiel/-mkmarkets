from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from .models import Profile


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': widgets.TextInput(attrs={
                'placeholder': 'John Doe'
            }),
            'password' : widgets.TextInput(attrs={
                'type': 'password',
                'placeholder': '1234567890'
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['balance']


class AccountGenerateForm(forms.Form):
    accounts = forms.IntegerField()
