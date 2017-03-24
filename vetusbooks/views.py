from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm, ImageUploadForm
from .util import getUserBooks
from django.http import HttpResponseRedirect, HttpResponse

class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = UserLoginForm(request.GET)
		img_form = ImageUploadForm()
		context={
			"user" : request.user,
			"form" : form,
			"img_form" : img_form
		}
		if(request.user.is_authenticated):
			context['user_books'] = getUserBooks(request.user)
		return render(request,"vetusbooks/home.html",context)
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
				form = UserLoginForm()
				context = {
					"form":form,
					"login_error":"Failed!"
				}
				return render(request,"vetusbooks/home.html",context)
			return HttpResponseRedirect("/")


class LogoutView(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		context={}
		return HttpResponseRedirect("/")

class LoginSuccessView(View):
	def get(self, request, *args, **kwargs):
		context={}
		print(request.user.is_authenticated())
		if(request.user.is_authenticated()):
			return render(request,"registration/loginSuccess.html",context)
		return HttpResponseRedirect("/login")
class LoginFailureView(View):
	def get(self, request, *args, **kwargs):
		context={}
		return render(request,"registration/loginFailure.html",context)

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

def register_view(request):
	return render(request,"form.html",{})

def test_view(request):

	return render(request,"testing.html",{"form":UserLoginForm()})

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = ExampleModel.objects.get(pk=course_id)
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')