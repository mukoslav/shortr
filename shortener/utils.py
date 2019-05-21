import random
import string
import geoip2.database
import datetime

# random ip addresses from rs, ch and us respectively, given to choose from randomply if users ip gets to be 127.0.0.1
# because geoip could not resolve country from localhost ;)
IPS = ['109.111.245.210', '5.149.63.255', '3.103.255.255']

def code_generator(size=5, chars=string.digits+string.ascii_lowercase+string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def create_shortcode(instance, size=5):
    Klass = instance.__class__
    while 1:
        new_code = code_generator(size=size)
        if not Klass.objects.filter(url=new_code).exists():
            return new_code

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ip_and_country(request):
    client_ip = get_client_ip(request)
    if client_ip=='127.0.0.1':
        client_ip = random.choice(IPS)
    reader = geoip2.database.Reader('./GeoLite2-Country_20190514/GeoLite2-Country.mmdb')
    country = reader.country(client_ip).country.iso_code
    reader.close()
    return client_ip, country.lower()

# distribution of clicks over 24h period - whole lot of magic numbers, all of which essential for svg generation
def distribution(clicks):
    res = []
    dt = datetime.datetime.now(tz=datetime.timezone.utc)
    start = dt - datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
    end = start + datetime.timedelta(minutes=60)
    max_clicks = 0
    for i in range(24):
        click_nr = clicks.filter(created_at__range=(start, end)).count()
        if click_nr > max_clicks:
            max_clicks = click_nr
        res.append([f"{start.strftime('%H')}h", 690-i*30, 0, click_nr, click_nr])
        start, end = start-datetime.timedelta(minutes=60), start
    for k in res:
        k[3] = k[3]/max_clicks * 200
        k[2] = 215 - k[3]
    return res
