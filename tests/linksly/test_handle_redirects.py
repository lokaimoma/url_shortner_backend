# Created by Kelvin_Clark on 6/17/22, 8:07 AM
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.linksly.models import URL
from tests import factories


class TestHandleRedirects(TestCase):
    def test_no_url(self):
        r = self.client.get(path=reverse('handle_redirects', kwargs={'code': 'xyz'}))
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_exist(self):
        url = factories.URLFactory()
        redirect_count = url.redirects
        r = self.client.get(path=reverse('handle_redirects', kwargs={'code': url.code}), follow=False)
        self.assertEquals(r.status_code, status.HTTP_307_TEMPORARY_REDIRECT)
        self.assertIn('Location', r.headers.keys())
        self.assertEquals(r.headers['Location'], url.long_url)
        url.refresh_from_db()
        self.assertEquals(url.redirects, redirect_count + 1)

    def test_urls_exist_not_active(self):
        url = factories.URLFactory()
        url.status = URL.status_choices[1][0]
        url.save()
        r = self.client.get(path=reverse('handle_redirects', kwargs={'code': url.code}))
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)
