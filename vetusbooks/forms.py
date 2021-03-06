from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage

from vetusbooks.models import User, Book

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
            'class': 'form-control'
            })
    username = forms.CharField(max_length=50, required=True,
    	widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})
    	)
    password = forms.CharField(required=True,
    	widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    	)

    def clean_username(self):
        uname = self.cleaned_data['username']
        if not User.objects.filter(username=uname) :
            raise forms.ValidationError("Invalid Username")
        return uname
    # def clean_password(self):
    #     uname = self.cleaned_data['username']
    #     pwd = self.cleaned_data['username']
    #     if User.objects.filter(username=uname).pass

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = {'username', 'password1', 'password2', 'email', 
                'phone', 'first_name', 'last_name', 'birth_date', 'location', 'avatar'}
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
            'password1'    : forms.TextInput(attrs = {'placeholder': 'Password'}),
            'password2'    : forms.TextInput(attrs = {'placeholder': 'Password'}),
            'email'    : forms.TextInput(attrs = {'placeholder': 'Email'}),
            'phone'    : forms.TextInput(attrs = {'placeholder': 'Phone Number'}),
            'first_name'    : forms.TextInput(attrs = {'placeholder': 'First Name'}),
            'last_name'    : forms.TextInput(attrs = {'placeholder': 'Last Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if(field in ['first_name','last_name']):
                self.fields[field].widget.attrs.update({
            'class': 'form-control form-ctrl'
            })
            else:
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

    # def clean(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Both Passwords Should Match")
    #     return password2
    def clean_username(self):
        uname = self.cleaned_data['username']
        if len(uname) < 5 :
            raise forms.ValidationError("Length of Username must be greater than 5")
        return uname

    def clean_email(self):
        email = self.cleaned_data['email']
        for user in User.objects.all():
            if user.email == email:
                raise forms.ValidationError("User with this Email already exists.")
        return email
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
        uname = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=uname).count():
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

class SellBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SellBookForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
            'class': 'form-control'
            })

    class Meta:
        model = Book
        fields = {
            'title', 'author', 'price', 'thumbnail','description',
        }

    def save(self, commit=True):
        new_book = super(SellBookForm, self).save(commit=False)
        new_book.title = self.cleaned_data['title']
        new_book.author = self.cleaned_data['author']
        new_book.price = self.cleaned_data['price']
        new_book.thumbnail = self.cleaned_data['thumbnail']
        new_book.description = self.cleaned_data['description']
        # if commit:
        #     new_user.save()
        return new_book