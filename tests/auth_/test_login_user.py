# Created by Kelvin_Clark on 4/26/22, 8:46 AM
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tests.factories import UserFactory


class TestLoginUser(TestCase):
    def test_invalid_payload(self):
        r = self.client.post(path=reverse('login'), data={'username': 'something', 'pwd': 'something'})
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_registered_user_with_provided_cred(self):
        r = self.client.post(path=reverse('login'), data={'username': 'something', 'password': 'something'})
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_exists_wrong_creds(self):
        u: User = UserFactory()
        r = self.client.post(path=reverse('login'), data={'username': u.username, 'password': 'something'})
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_exists_correct_creds(self):
        u: User = UserFactory()
        r = self.client.post(path=reverse('login'), data={'username': u.username, 'password': 'hello'})
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        j = r.json()
        self.assertEquals(j['username'], u.username)
        self.assertEquals(j['firstName'], u.first_name)
        self.assertEquals(j['lastName'], u.last_name)
        self.assertEquals(j['email'], u.email)
        self.assertIn('access', j.keys())
        self.assertIn('refresh', j.keys())
        self.assertIsNotNone(j['access'])
        self.assertIsNotNone(j['refresh'])
