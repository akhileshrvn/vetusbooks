
from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth import logout, authenticate, login

from django.utils.http import urlencode

from .forms import UserLoginForm, ImageUploadForm, RegistrationForm, ContactForm
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
			register_form = RegistrationForm()
			context["register_form"] = register_form
			return render(request,'registration/registration.html',context)
	def post(self, request, *args, **kwargs):
		form = register_form(request.POST)
		context = {
			"title" : "Register",
			"register_form" : form
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

def sendMail(request):
	if request.method == "POST":
		mail_form = ContactForm(request.POST)
		if mail_form.is_valid():
			subject = mail_form.cleaned_data['subject']
			message = mail_form.cleaned_data['message']
			sender = mail_form.cleaned_data['sender']
			cc_myself = mail_form.cleaned_data['cc_myself']
			recipients = ['tgmukku@softpathtech.com']
			if cc_myself:
				recipients.append(sender)

			send_mail(subject, message, sender, recipients)
			return HttpResponseRedirect('/thanks/')
	else:
		mail_form = ContactForm()
	return render(request, 'name.html', {'mail_form':mail_form})

def register(request):
	if request.method == "POST":
		register_form = RegistrationForm(request.POST)
		if(request.user.is_authenticated()):
			HttpResponseRedirect("/")
		if register_form.is_valid():
			new_user = register_form.save()
			username = register_form.cleaned_data['username']
			password = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']
			user = authenticate(username=username, password=password)
			print("UNAME",user)
			# login(request, user)
			return HttpResponse("User Created Successfully!")
	else:
		register_form = RegistrationForm()
	return render(request, 'registration/registration.html', {'register_form' : register_form})