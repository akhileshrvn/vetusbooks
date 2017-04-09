
from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth import logout, authenticate, login

from django.utils.http import urlencode

from .forms import UserLoginForm, ImageUploadForm, RegistrationForm, ContactForm, UserProfileForm
from .util import getUserBooks, handleLogin
from .models import Book,User
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail

class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = UserLoginForm(request.GET)
		img_form = ImageUploadForm()
		context={
			"title" : "Home",
			"img_form" : img_form,
			"login_form" : form,
		}
		handleLogin(request, context, form)
		if(request.user.is_authenticated):
			context['user_books'] = getUserBooks(request.user)
		return render(request,"vetusbooks/home.html",context)
	def post(self, request, *args, **kwargs):
		form = UserLoginForm(request.POST)
		context = {
			"title" : "Home",
			"login_form" : form
		}
		handleLogin(request, context, form)
		return render(request,"vetusbooks/home.html",context)
class LogoutView(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		context={}
		return HttpResponseRedirect("/")

class LoginView(View):
	def get(self, request, *args, **kwargs):
		current_user = request.user
		if(current_user.is_authenticated()):
			return HttpResponseRedirect("/")
		else:
			form = UserLoginForm()
			context = {
				"title" : "Log In!",
				"form" : form
			}
		return render(request,'registration/login.html',context)
	def post(self, request, *args, **kwargs):
		form = UserLoginForm(request.POST)
		context = {
			"title" : "Log In!",
			"form" : form
		}
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request,user)
				return HttpResponseRedirect("/")
			else:
				raise forms.ValidationError("You cannot post more than once every x minutes")
			return HttpResponseRedirect("/")

class SearchView(View):
	def get(self, request, *args, **kwargs):
		form = UserLoginForm(request.GET)
		context = {
			"title": "Search",
			"login_form" : form
		}
		handleLogin(request, context, form)
		srch_book_name = request.GET.get('srch-book')
		if srch_book_name is None:
			return render(request,"vetusbooks/home.html",context)
		search_result = Book.objects.filter(title__contains=srch_book_name)
		context['search_result'] = search_result
		return render(request,"vetusbooks/search.html",context)
	def post(self, request, *args, **kwargs):
		form = UserLoginForm(request.POST)
		context = {
			"form" : form
		}
		handleLogin(request, context, form)
		return HttpResponseRedirect("/")

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'vetusbooks/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'vetusbooks/simple_upload.html')


def register(request):
	context = {
			"title": "Sign Up!",
	}
	if(request.user.is_authenticated):
		return HttpResponseRedirect("/")
	if request.method == "POST":
		register_form = RegistrationForm(request.POST, request.FILES)
		if register_form.is_valid():
			new_user = register_form.save()
			print("USER AVATAR", new_user.avatar)
			username = register_form.cleaned_data['username']
			password = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']

			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect("/")
	else:
		register_form = RegistrationForm()
	context["register_form"] = register_form
	return render(request, 'registration/registration.html', context)

def user_profile(request):
	context = {
			"title": "Profile",
	}
	if(not request.user.is_authenticated()):
		return HttpResponseRedirect("/")
	if request.method == "POST":
		profile_form = UserProfileForm(request.POST, request.FILES, instance = request.user)
		if profile_form.is_valid():
			print("Avatar" , profile_form.cleaned_data['avatar'])
			new_user = profile_form.save()
			print("Avatar 2", new_user.avatar)
			context["alert_message"] = "Profile Updated Successfully!"
			print("context updated")
			return HttpResponseRedirect("/profile", context)
	else:
		print("Not Valid")
		profile_form = UserProfileForm(instance=request.user)
	context["profile_form"] = profile_form
	return render(request, 'registration/user_profile.html', context)

def user_books(request):
	if(not request.user.is_authenticated()):
		return HttpResponseRedirect("/")
	else:
		context = {
			"title" : "My Books",
			"user_books" : getUserBooks(request.user)
		}

	return render(request, 'vetusbooks/user_books.html', context)

def sell_book(request):
	if(not request.user.is_authenticated()):
		return HttpResponseRedirect("/")
	else:
		context = {
			"title" : "Sell Book",
		}

	return render(request, 'vetusbooks/sell_book.html', context)

def testing(request):
	return render(request, 'testing.html', {})