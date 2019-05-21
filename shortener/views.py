from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from shortener.models import ShortURL, Link, Click
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .utils import get_ip_and_country, get_client_ip, distribution
import random


def create_new_short_link(request):
    return redirect(ShortURL.objects.create(user_id=request.user.id))

def short_url_detail_view(request, id):
    short_url = get_object_or_404(ShortURL,pk=id)
    links = Link.objects.filter(shorturl_id=id)
    clicks = Click.objects.filter(shorturl_id=id)
    countries = clicks.values('country').distinct().count()
    users = clicks.values('ip').distinct().count()
    dist = distribution(clicks) if clicks else None
    context = { 'short_url': short_url,'links': links,'clicks': clicks,'countries': countries,'users': users,'distribution': dist }
    return render(request, 'shortener/short_url_detail.html', context=context)

def create_new_link(request, id):
    url = request.POST['url']
    weight = None if request.POST['weight'] == "" else float(request.POST['weight'])
    active = 'active' in request.POST.keys()
    country_specific = request.POST['country_specific']
    link = Link.objects.create(shorturl_id=id,url=url,weight=weight,active=active,country_specific=country_specific)
    return redirect(ShortURL.objects.get(pk=id))

def remove_link(request, id):
    link = get_object_or_404(Link,pk=id)
    short_url = ShortURL.objects.get(id=link.shorturl_id)
    link.delete()
    return redirect(short_url)

def update_default_link(request, id):
    obj = ShortURL.objects.get(pk=id)
    obj.default = request.POST['default']
    obj.active = 'active' in request.POST.keys()
    obj.save()
    return redirect(obj)

def link_detail_view(request, id):
    link = get_object_or_404(Link,pk=id)
    return render(request, 'shortener/link_detail.html', context={'link': link})

def update_link(request, id):
    link = get_object_or_404(Link,pk=id)
    link.url = request.POST['url']
    link.weight = None if request.POST['weight'] == "" else float(request.POST['weight'])
    link.active = 'active' in request.POST.keys()
    link.country_specific = request.POST['country_specific']
    link.save()
    short_url = ShortURL.objects.get(id=link.shorturl_id)
    return redirect(short_url)

# logic seems overkill-ishly but it handles all the cases (weights do not add up to 1, some links weighted some not, etc.)
def short_url_redirect(request, shorturl=None, *args, **kwargs):
    obj = get_object_or_404(ShortURL, url=shorturl)
    if not obj.active:
        return HttpResponseNotFound('Link not activated!')
    client_ip, country = get_ip_and_country(request)
    specific = Link.objects.filter(country_specific__contains=country).filter(shorturl_id=obj.id).filter(active=True)
    non_specific = Link.objects.filter(country_specific='').filter(shorturl_id=obj.id).filter(active=True)
    links = specific or non_specific
    redirect_link = choose_link(links) if links else obj.default
    if redirect_link==None:
        return HttpResponseNotFound('Weights are not distributed properly!')
    click = create_click(client_ip,country,obj.id,redirect_link.id if links else 0)
    return HttpResponseRedirect(redirect_link.url if links else redirect_link)

def create_click(ip, country, shorturl_id, link_id):
    Click.objects.create(ip=ip,country=country,shorturl_id=shorturl_id,link_id=link_id)
    return

# e.g. say we have 4 links with weights 0.5, 0.3, None, None. probability is 0.8 that link will be chosen.
# if not we then take a pick randomly from non weighted links.
# actual probabilities for links would be dispersed thus, 0.5, 0.3, 0.1, 0.1
def choose_link(links):
    rnd = random.uniform(0, 1)
    weighted = links.exclude(weight=None)
    non_weighted = links.filter(weight=None)
    for w in weighted:
        rnd -= w.weight
        if rnd < 0:
            return w
    return random.choice(non_weighted) if non_weighted else None

def get_clicks(request, shorturl_id):
    result = Click.objects.filter(shorturl_id=shorturl_id).order_by('id')
    return render(request,'shortener/clicks_index.html', {'clicks': result, 'shorturl_id': shorturl_id})

def get_clicks_by_ip(request, shorturl_id, ip):
    result = Click.objects.filter(shorturl_id=shorturl_id).filter(ip=ip)
    return render(request,'shortener/clicks_by_ip.html', {'clicks': result})
