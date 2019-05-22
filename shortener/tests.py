from django.test import TestCase, Client, RequestFactory
from shortener.models import ShortURL, Link, Click
from user.models import User
from shortener.views import create_new_short_link, short_url_redirect


class ShortURLTestCase(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(username='gor3n',
                                             email='ndelevic@yahoo.com',
                                             password='passpass')
        self.short_url = ShortURL.objects.create(user_id=self.user.id,
                                                 active=True)
        self.default_link = Link.objects.create(short_url_id=self.short_url.id,
                                                url='google.com',
                                                active=True,
                                                default=True,
                                                country_specific='rs, ch, us',
                                                weight=0.4)
        self.link1 = Link.objects.create(short_url_id=self.short_url.id,
                                         url='facebook.com',
                                         active=True,
                                         country_specific='rs, ch, us',
                                         weight=0.4)
        self.link2 = Link.objects.create(short_url_id=self.short_url.id,
                                         url='github.com',
                                         active=True,
                                         country_specific='rs, ch, us',
                                         weight=0.6)
        self.client.login(username='gor3n', password='passpass')

    def test_short_url_generated(self):
        self.assertNotEqual(self.short_url, None)


    def test_redirects_to_short_url_upon_generation(self):
        request = self.request_factory.post('/shortener/')
        request.user = self.user
        response = create_new_short_link(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/shortener/shorturl/{ShortURL.objects.last().id}')


    def test_redirects_to_link(self):
        response = self.client.post(f'/{self.short_url.url}')
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.url, ['facebook.com', 'github.com'])


    def test_add_new_landing_page_and_redirect_back_to_short_url(self):
        params = {'short_url_id': self.short_url.id,
                  'url': 'youtube.com',
                  'active':True,
                  'country_specific': 'rs, ch, us',
                  'weight': 0.2}
        response = self.client.post(f'/shortener/shorturl/{self.short_url.id}/new_link', params)
        self.link3 = Link.objects.get(url='youtube.com')
        for k, v in params.items():
            self.assertEqual(getattr(self.link3,k), v)
        self.assertEqual(response.url, f'/shortener/shorturl/{ShortURL.objects.last().id}')


    def test_update_landing_page(self):
        params = self.link2.__dict__
        params['weight'] = 0.4
        response = self.client.post(f'/shortener/link/{self.link2.id}/update_link', params)
        self.assertEqual(self.link2.weight, 0.4)
        self.assertEqual(response.url, f'/shortener/shorturl/{self.link2.short_url_id}')


    def test_redirect_to_default_page_if_active_alternatives(self):
        self.link1.active = False
        self.link2.active = False
        self.link1.save()
        self.link2.save()
        response = self.client.post(f'/{self.short_url.url}')
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.url, ['google.com'])
