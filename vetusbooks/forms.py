from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True,
    	widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
    	)
    password = forms.CharField(required=True,
    	widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    	)

class UserRegistrationForm(forms.Form):
	username = forms.CharField(max_length=50, required=True,
		widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
		)
	password = forms.CharField(required=True,
    	widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    	)

class ImageUploadForm(forms.Form):
	image = forms.ImageField()