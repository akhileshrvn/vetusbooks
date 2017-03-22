from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)