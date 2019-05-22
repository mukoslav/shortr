from django.db import models
from django.urls import reverse
from user.models import User
from .utils import code_generator, create_shortcode


class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=5, unique=True, default=None)
    active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.url == None:
            self.url = create_shortcode(self)
        super(ShortURL, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shortener:short_url_detail', kwargs={'id': self.id})

    def __str__(self):
        return str(self.url)


class Link(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    url = models.CharField(max_length=220)
    country_specific = models.CharField(max_length=20, default=None)
    weight = models.FloatField(null=True, blank=True, default=None)
    active = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.url)


class Click(models.Model):
    ip = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.ip)
