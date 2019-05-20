from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from user import views
from shortener.views import short_url_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^user/',include('user.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^shortener/',include('shortener.urls')),
    url(r'^(?P<shorturl>[\a-zA-Z0-9]+){0,5}$',short_url_redirect)
]
