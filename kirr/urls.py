
from django.conf.urls import include

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from vetusbooks import views
urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/$', views.user_profile, name='view_profile'),
    url(r'^seller/(?P<id>\d+)/$', views.seller_profile, name='seller_profile'),
    url(r'^sell_book/$', views.sell_book, name='sell_book'),
    url(r'^user_books/$', views.user_books, name='user_books'),
    url(r'^testing/$', views.testing, name='testing'),
    url(r'^book/(?P<book_id>\d+)/$', views.show_book, name='show_book'),
    url(r'^remove_book/(?P<book_id>\d+)/$', views.remove_book, name='remove_book'),
    url(r'^send_message/(?P<book_id>\d+)/(?P<sender_id>\d+)/(?P<book_owner_id>\d+)/$', views.send_message, name='send_message'),
    # url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='scode'),
]

#..rest of url.py config...
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)