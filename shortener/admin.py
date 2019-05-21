from django.contrib import admin
from .models import ShortURL, Link, Click

admin.site.register([ShortURL, Link, Click])
