from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage

from vetusbooks.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True,
    	widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
    	)
    password = forms.CharField(required=True,
    	widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    	)

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = {'username', 'password1', 'password2', 'email', 
                'phone', 'first_name', 'last_name', 'birth_date', 'location', 'avatar'}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
            'class': 'form-control'
            })
    def save(self, commit=True):
        new_user = super(RegistrationForm, self).save(commit=False)
        new_user.email = self.cleaned_data['email']
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.phone = self.cleaned_data['phone']
        new_user.birth_date = self.cleaned_data['birth_date']
        new_user.avatar = self.cleaned_data['avatar']
        if commit:
            new_user.save()
        return new_user

    def clean_username(self):
        uname = self.cleaned_data['username']
        if len(uname) < 5 :
            raise forms.ValidationError("Length of Username must be greater than 5")
        return uname

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
            'class': 'form-control'
            })

    class Meta:
        model = User
        fields = {
            'username', 'email', 'first_name', 'last_name','phone', 'avatar', 'location'
        }

    def clean_username(self):
        uname = self.cleaned_data['username']
        if len(uname) < 5 :
            raise forms.ValidationError("Length of Username must be greater than 5")
        return uname

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        print("Getting")
        user = super(UserProfileForm, self).save(commit=False)
        print("NEW Avatar" , user.avatar.url)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.avatar = self.cleaned_data['avatar']
        print("Avatar" , user.avatar.url)
        if commit:
            user.save()
        return user

class ImageUploadForm(forms.Form):
	image = forms.ImageField()


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if len(subject) < 5:
            raise forms.ValidationError("Length of subject must be greater than 5")
        return subject