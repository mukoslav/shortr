from django.shortcuts import render, get_object_or_404, redirect
from shortener.models import ShortURL, Link, Click
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .utils import get_ip_and_country, get_client_ip, distribution
import random
from .decorators import user_is_instance_owner
import code # code.interact(local=dict(globals(), **locals()))


def create_new_short_link(request):
    short_url = ShortURL.objects.create(user=request.user)
    Link.objects.create(short_url=short_url,
                        default=True,
                        url='https://google.com',
                        active=True,
                        country_specific='')
    return redirect(short_url)


@user_is_instance_owner
def short_url_detail_view(request, id):
    short_url = get_object_or_404(ShortURL,pk=id)
    links = short_url.link_set.filter(default=False)
    default_link = short_url.link_set.get(default=True)
    clicks = short_url.click_set.all()
    countries = clicks.values('country').distinct().count()
    users = clicks.values('ip').distinct().count()
    dist = distribution(clicks) if clicks else None
    shared_link = f'{request.get_host()}/{short_url.url}'
    context = {
                'short_url': short_url,
                'links': links,
                'default_link': default_link,
                'clicks': clicks,
                'countries': countries,
                'users': users,
                'distribution': dist,
                'shared_link': shared_link
              }
    return render(request, 'shortener/short_url_detail.html', context=context)


@user_is_instance_owner
def create_new_link(request, id):
    url = request.POST['url']
    weight = float(request.POST['weight']) if request.POST['weight'] else None
    active = 'active' in request.POST.keys()
    country_specific = request.POST['country_specific'].lower()
    link = Link.objects.create(short_url_id=id,
                               url=url,
                               weight=weight,
                               active=active,
                               country_specific=country_specific)
    return redirect(link.short_url)


@user_is_instance_owner
def remove_link(request, id):
    link = get_object_or_404(Link,pk=id)
    link.delete()
    return redirect(link.short_url)


@user_is_instance_owner
def update_default_link(request, id):
    link = get_object_or_404(Link,pk=id)
    link.url = request.POST['default']
    link.save()
    return redirect(link.short_url)


@user_is_instance_owner
def link_detail_view(request, id):
    link = get_object_or_404(Link,pk=id)
    return render(request, 'shortener/link_detail.html', context={'link': link})


@user_is_instance_owner
def update_link(request, id):
    link = get_object_or_404(Link,pk=id)
    link.url = request.POST['url']
    link.weight = float(request.POST['weight']) if request.POST['weight'] else None
    link.active = 'active' in request.POST
    link.country_specific = request.POST['country_specific'].lower()
    link.save()
    return redirect(link.short_url)


@user_is_instance_owner
def toggle_short_link_active(request, id):
    # code.interact(local=dict(globals(), **locals()))
    short_url = get_object_or_404(ShortURL,pk=id)
    short_url.active ^= True
    short_url.save()
    return redirect(short_url)


# logic seems overkill-ishly but it handles all the cases (weights do not add up to 1, some links weighted some not, etc.)
def short_url_redirect(request, shorturl=None, *args, **kwargs):
    short_url = get_object_or_404(ShortURL, url=shorturl, active=True)
    client_ip, country = get_ip_and_country(request)
    ls = short_url.link_set
    specific = ls.filter(country_specific__contains=country, active=True, default=False)
    non_specific = ls.filter(country_specific='', active=True, default=False)
    default = ls.get(default=True)
    redirect_link = choose_link(specific or non_specific) or default
    click = create_click(client_ip,country,short_url.id,redirect_link.id)
    return HttpResponseRedirect(redirect_link.url)


# e.g. say we have 4 links with weights 0.5, 0.3, None, None. probability is 0.8 that link will be chosen.
# if not we then take a pick randomly from non weighted links.
# actual probabilities for links would be dispersed thus, 0.5, 0.3, 0.1, 0.1
def choose_link(links):
    weighted = links.exclude(weight=None)
    non_weighted = links.filter(weight=None)
    rnd = random.uniform(0, 1)
    for w in weighted:
        rnd -= w.weight
        if rnd < 0:
            return w
    return random.choice(non_weighted) if non_weighted else None


def create_click(ip, country, short_url_id, link_id):
    Click.objects.create(ip=ip, country=country, short_url_id=short_url_id, link_id=link_id)
    return


def get_clicks(request, short_url_id):
    result = Click.objects.filter(short_url_id=short_url_id).order_by('id')
    return render(request,'shortener/clicks_index.html', {'clicks': result, 'short_url_id': short_url_id})


def get_clicks_by_ip(request, short_url_id, ip):
    result = Click.objects.filter(short_url_id=short_url_id).filter(ip=ip)
    return render(request,'shortener/clicks_by_ip.html', {'clicks': result})
