
from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth import logout

from django.utils.http import urlencode

from .forms import UserLoginForm, ImageUploadForm
from .util import getUserBooks, handleLogin
from .models import Book,User
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage


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

class RegistrationView(View):
	def get(self, request, *args, **kwargs):
		current_user = request.user
		login_form = UserLoginForm(request.GET)
		context = {
			"title" : "Registration"
		}
		handleLogin(request, context, login_form)
		if(current_user.is_authenticated()):
			return HttpResponse("Already Logged In")
		else:
			register_form = RegistrationView()
			context["register_form"] = register_form
			return render(request,'registration/registration.html',context)
	def post(self, request, *args, **kwargs):
		form = register_form(request.POST)
		context = {
			"title" : "Register",
			"regiser_form" : form
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