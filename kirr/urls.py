
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from shortener.views import URLRedirectView
from vetusbooks.views import testing, simple_upload,SearchView, LogoutView, HomeView, register, user_profile, user_books, sell_book
urlpatterns = [
	url(r'^upload/$', simple_upload),
	url(r'^search/$', SearchView.as_view(), name='search'),
	url(r'^register/$', register, name='search'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^profile/$', user_profile, name='view_profile'),
    url(r'^sell_book/$', sell_book, name='sell_book'),
    url(r'^user_books/$', user_books, name='user_books'),
    url(r'^testing/$', testing, name='user_books'),
    # url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='scode'),
]

#..rest of url.py config...
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)