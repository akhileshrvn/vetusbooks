
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from shortener.views import URLRedirectView
from vetusbooks.views import test_view, upload_pic, LogoutView, LoginView, LoginSuccessView, LoginFailureView,HomeView
urlpatterns = [
	url(r'^testing/$', test_view, name='upload'),
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='scode'),
]