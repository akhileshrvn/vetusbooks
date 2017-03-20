from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent
from .forms import SubmitURLForm
from .models import KirrURL
# Create your views here.

class HomeView(View):
	def get(self,request, *args, **kwargs):
		the_form = SubmitURLForm()
		context = {
			"title": "Kirr.co",
			"form": the_form
		}
		return render(request, "shortener/home.html", context)

	def post(self, request, *args, **kwargs):
		form = SubmitURLForm(request.POST)
		context = {
			"title": "Kirr.co",
			"form": form
		}
		template = "shortener/home.html"
		if form.is_valid():
			new_url = form.cleaned_data.get("url")
			obj, created = KirrURL.objects.get_or_create(url=new_url)
			context = {
				"object":obj,
				"created":created,
			}
			if created:
				template = "shortener/success.html"
			else:
				template = "shortener/already-exists.html"
		return render(request, template, context)

class URLRedirectView(View):	# class based view
	def get(self, request, shortcode=None, *args, **kwargs):
		print(shortcode)
		qs = KirrURL.objects.filter(shortcode=shortcode)
		# if qs.count !=1 and qs.exists():
		# 	raise Http404
		obj = get_object_or_404(KirrURL, shortcode=shortcode)
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)

