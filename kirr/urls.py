
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from shortener.views import URLRedirectView
from vetusbooks.views import simple_upload,SearchView, LogoutView, HomeView, register, sendMail
urlpatterns = [
	url(r'^sendmail/$', sendMail),
	url(r'^upload/$', simple_upload),
	url(r'^search/$', SearchView.as_view(), name='search'),
	url(r'^register/$', register, name='search'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    # url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='scode'),
]