from django.shortcuts import render
from django import forms
from django.views import View
from django.contrib.auth import logout, authenticate, login

from django.utils.http import urlencode

from .forms import UserLoginForm, ImageUploadForm, RegistrationForm, ContactForm, UserProfileForm, SellBookForm
from .util import getUserBooks, handleLogin
from .models import Book,User
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.db.models import Q

# for paypal
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm

import os

def home_view(request):
	context={
		"title" : "Home",
		}
	if(request.user.is_authenticated):
		context["random_books"] = Book.objects.all().filter(~Q(seller_id = request.user.id)).order_by('?')[:12]
	else:
		 context["random_books"] = Book.objects.all().order_by('?')[:12]
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
				"login_form" : form,
			}
		return render(request,'registration/login_2.html',context)
	def post(self, request, *args, **kwargs):
		form = UserLoginForm(request.POST)
		context = {
			"title" : "Log In!",
			"login_form" : form
		}
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request,user)
				return HttpResponseRedirect("/")
			else:
				context['login_error'] = "Login Failed!"
		return render(request, 'registration/login_2.html',context)

class SearchView(View):
	def get(self, request, *args, **kwargs):
		form = UserLoginForm(request.GET)
		context = {
			"title": "Search",
			"login_form" : form
		}
		srch_book_name = request.GET.get('srch-book')
		if srch_book_name is None:
			return render(request,"vetusbooks/home.html",context)
		search_result = Book.objects.filter(title__contains=srch_book_name)
		context['search_result'] = search_result
		context['search_length'] = len(search_result)
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
			username = register_form.cleaned_data['username']
			password = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']
			user = authenticate(username=username, password=password)
			login(request, user)
			context = {
				"title" : "Profile",
				"alert_message" : "Hurray! Registered Successfully",
			}
			return HttpResponseRedirect("/user_books")
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
			new_user = profile_form.save()
			context["alert_message"] = "Profile Updated Successfully!"
			context["profile_form"] = profile_form
			return render(request, "registration/user_profile.html", context)
	else:
		profile_form = UserProfileForm(instance=request.user)
	context["profile_form"] = profile_form
	return render(request, 'registration/user_profile.html', context)

def seller_profile(request, id):
	user = User.objects.filter(id=id)
	if user:
		user = user[0]
	else:
		HttpResponseRedirect("/")
	context = {
			"title": user.username,
			"user" : user
	}
	return render(request, 'vetusbooks/seller_profile.html', context)

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
	context = {
		"title": "Sell Book!",
	}
	if(not request.user.is_authenticated):
		return HttpResponseRedirect("/")
	if request.method == "POST":
		book_form = SellBookForm(request.POST, request.FILES)
		if book_form.is_valid():
			new_book = book_form.save()
			new_book.seller_id = request.user.id
			new_book.save()
			context['alert_message'] = new_book.title + " Added Successfully!"
			context['user_books'] = getUserBooks(request.user)
			return render(request, 'vetusbooks/user_books.html', context)
	else:
		book_form = SellBookForm()
	context["book_form"] = book_form
	return render(request, 'vetusbooks/sell_book.html', context)

def testing(request):
	
	paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
        "return_url": "/",
        "cancel_return": "/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}
	return render(request, 'payment.html', context)

def show_book(request, book_id):
	result_book = Book.objects.filter(id=book_id)
	if not result_book:
		return HttpResponseRedirect("/")
	result_book = result_book[0]
	paypal_dict = {
        "business": "vetusbooks.app@gmail.com",
        "amount": result_book.price,
        "item_name": result_book.title,
        "invoice": "unique-invoice-id",
        "notify_url": "http://localhost:8000/paypal/" + reverse('paypal-ipn'),
        "return_url": "http://localhost:8000/book/"+str(result_book.id),
        "cancel_return": "http://localhost:8000/book/"+str(result_book.id),
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
	payment_form = PayPalPaymentsForm(initial=paypal_dict)
	context = {
		"title":result_book.title,
		"result_book": result_book,
		"user" : request.user,
		"seller" : User.objects.filter(id=result_book.seller_id)[0],
		"payment_form" : payment_form
	}
	return render(request, 'vetusbooks/show_book.html',context)

def remove_book(request, book_id):
	book = Book.objects.filter(id=book_id)
	if not book:
		return HttpResponseRedirect("/")
	book = book[0]
	user = request.user
	context = {
		"title":"Delete "+ book.title,
		"book": book,
		"user" : user
	}
	if(user.is_authenticated() and user.id == book.seller_id):
		os.remove(book.thumbnail.path)
		book.delete()
		context["alert_message"] = book.title + " Deleted Successfully!"
		context["user_books"] = getUserBooks(request.user)
		return render(request, "vetusbooks/user_books.html", context)
	else:
		return HttpResponseRedirect("/")

def send_message(request, book_id, sender_id, book_owner_id):
	book = Book.objects.filter(id=book_id)
	sender = User.objects.filter(id=sender_id)
	book_owner = User.objects.filter(id=book_owner_id)
	if request.method == 'POST' and book and sender and book_owner and request.user.is_authenticated:
		book = book[0]
		sender = sender[0]
		book_owner = book_owner[0]
		user_message = request.POST.get('message')
		# message_text =  sender.firstname + " asking something about your book " + book.title
		# message_text += "\n" + user_message
		context = {
			"title":book.title,
			"result_book": book,
			"user" : request.user,
			"seller" : User.objects.filter(id=book.seller_id)[0],
			"alert_message" : "Message Sent Successfully!"
		}
		msg = EmailMessage(book_owner.username +" | " + book.title,
		get_template('vetusbooks/email.html').render(
			Context({
				'msg_sender': sender,
				'user_message': user_message,
				'sender_avatar' : "http://localhost:8000"+sender.avatar.url,
				'sender_profile' : "http://localhost:8000/seller/"+str(sender.id)+"/"
				})
			),
		'vetusbooks.app@gmail.com',
		 [book_owner.email])
		msg.content_subtype = "html"
		msg.send()
		return render(request, "vetusbooks/show_book.html", context)
		# return HttpResponseRedirect(request.META.get('HTTP_REFERER'),{'alert_message':"Message Sent Successfully!"})
	else:
		return HttpResponseRedirect("/")

def about(request):
	return render(request, "vetusbooks/about_us.html",{"title":"About Us"})

def contact(request):
	return render(request, "vetusbooks/contact.html",{"title":"Contact Us"})