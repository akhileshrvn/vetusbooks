from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
def kirr_redirect_view(request, *args, **kwargs): # function based view
	return HttpResponse("Hello World!!!")

class KirrCBView(View):	# class based view
	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello World Again")