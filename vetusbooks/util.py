from .models import User,Book
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from .forms import UserLoginForm

def getUserBooks(user):
	return Book.objects.filter(seller_id=user.id)

def handleLogin(request, context, form):
	if form.is_valid():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request,user)
			context["user"] = request.user
			context["user_books"] = getUserBooks(request.user)
		else:
			context["login_error"] = "Failed!"