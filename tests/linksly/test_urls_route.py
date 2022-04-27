# Created by Kelvin_Clark on 4/27/22, 3:37 PM
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.linksly.models import URL
from tests import get_auth_headers, faker
from tests.factories import UserFactory, URLFactory


class TestURLSGETANDPermission(TestCase):
    def test_get_all_urls_no_auth_user(self):
        r = self.client.get(path=reverse('url-list'))
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_urls_valid_user(self):
        u = UserFactory()
        h = get_auth_headers(username=u.username, client=self.client)
        r = self.client.get(path=reverse('url-list'), **h)
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        j = r.json()
        self.assertIn('count', j.keys())
        self.assertIn('results', j.keys())

    def test_get_url_no_auth_user(self):
        r = self.client.get(path=reverse('url-detail', kwargs={'pk': 1}))
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_url_valid_user(self):
        url: URL = URLFactory()
        h = get_auth_headers(username=url.user.username, client=self.client)
        r = self.client.get(path=reverse('url-detail', kwargs={'pk': url.code}), **h)
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        j = r.json()
        self.assertEquals(j['code'], url.code)
        self.assertEquals(j['long_url'], url.long_url)


class TestAddURL(TestCase):

    def test_add_invalid_payload(self):
        u = UserFactory()
        h = get_auth_headers(username=u.username, client=self.client)
        payload = {'long_url9': faker.domain_name()}
        r = self.client.post(path=reverse('url-list'), data=payload, **h)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_url_valid_payload(self):
        u = UserFactory()
        h = get_auth_headers(username=u.username, client=self.client)
        payload = {'long_url': faker.domain_name()}
        r = self.client.post(path=reverse('url-list'), data=payload, **h)
        self.assertEquals(r.status_code, status.HTTP_201_CREATED)
        urls = URL.objects.filter(user_id=u.id)
        self.assertEquals(len(urls), 1)


class TestEditURL(TestCase):
    def test_edit_url(self):
        url: URL = URLFactory()
        h = get_auth_headers(username=url.user.username, client=self.client)
        payload = {'long_url': 'https://somenewurl.com'}
        r = self.client.put(path=reverse('url-detail', kwargs={'pk': url.code}), data=payload, **h,
                            content_type='application/json')
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        new_url = URL.objects.get(code=url.code)
        self.assertNotEquals(new_url.long_url, url.long_url)
        self.assertEquals(new_url.long_url, payload['long_url'])


class TestDeleteURL(TestCase):
    def test_delete_url(self):
        url: URL = URLFactory()
        h = get_auth_headers(username=url.user.username, client=self.client)
        r = self.client.delete(path=reverse('url-detail', kwargs={'pk': url.code}), **h)
        self.assertEquals(r.status_code, status.HTTP_204_NO_CONTENT)
        urls = URL.objects.filter(user_id=url.user.id)
        self.assertEquals(len(urls), 0)