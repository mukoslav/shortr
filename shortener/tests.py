from django.test import TestCase, Client, RequestFactory
from shortener.models import ShortURL, Link, Click
from user.models import User
from shortener.views import create_new_short_link, short_url_redirect


class ShortURLTestCase(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(username='gor3n', email='ndelevic@yahoo.com', password='passpass')
        self.short_url = ShortURL.objects.create(user_id=self.user.id, default='google.com', active=True)
        self.link1 = Link.objects.create(shorturl_id=self.short_url.id, url='pornhub.com', active=True, country_specific='rs', weight=0.4)
        self.link2 = Link.objects.create(shorturl_id=self.short_url.id, url='github.com', active=True, country_specific='rs', weight=0.6)

    def test_short_url_generated(self):
        self.assertNotEqual(self.short_url, None)

    def test_redirects_to_short_url_upon_generation(self):
        request = self.request_factory.post('/shortener/')
        request.user = self.user
        response = create_new_short_link(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/shortener/short_url/{ShortURL.objects.all().last().id}')

    # def test_redirects_to_link(self):
    #     response = self.client.post(f'/{self.short_url.url}')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, 302)
