from django.db import models
from django.urls import reverse
from .utils import code_generator, create_shortcode


class ShortURL(models.Model):
    user_id = models.IntegerField(default=0)
    url = models.CharField(max_length=5, unique=True, default=None)
    default = models.CharField(max_length=200, default='https://google.com')
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
    shorturl_id = models.IntegerField(default=0)
    url = models.CharField(max_length=220)
    country_specific = models.CharField(max_length=20, default=None)
    weight = models.FloatField(null=True, blank=True, default=None)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(" | url: " + self.url + " | weight: " + str(self.weight) + " | country_specific: " + self.country_specific + " | active: " + str(self.active))


class Click(models.Model):
    ip = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    shorturl_id = models.IntegerField(default=0)
    link_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.ip)
