
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from shortener.views import URLRedirectView
from vetusbooks.views import SearchView, LogoutView, HomeView, RegistrationView
urlpatterns = [
	url(r'^search/$', SearchView.as_view(), name='search'),
	url(r'^register/$', RegistrationView.as_view(), name='search'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    # url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='scode'),
]