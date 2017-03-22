from django.shortcuts import render
from django.views import View
from .forms import UserLoginForm
from django.contrib.auth import authenticate,login, logout

from django.http import HttpResponseRedirect, HttpResponse

class HomeView(View):
	def get(self, request, *args, **kwargs):
		context={
			"user" : request.user
		}
		return render(request,"vetusbooks/home.html",context)

class LogoutView(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		context={}
		return render(request,"registration/logout.html",context)

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
		return HttpResponseRedirect("/")

def register_view(request):
	return render(request,"form.html",{})

def logout_view(request):
	return render(request,"form.html",{})
