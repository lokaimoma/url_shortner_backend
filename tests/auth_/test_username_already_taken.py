# Created by Kelvin_Clark on 4/21/22, 6:01 PM
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from tests.factories import UserFactory


class TestUserNameAlreadyTaken(TestCase):
    def test_no_query(self):
        r = self.client.get(path=f"{reverse('check-user-name-exists')}")
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_uname_empty(self):
        r = self.client.get(path=f"{reverse('check-user-name-exists')}?username=")
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_uname_already_taken(self):
        u = UserFactory()
        r = self.client.get(path=f"{reverse('check-user-name-exists')}?username={u.username}")
        self.assertTrue(r.json()['taken'])

    def test_uname_not_taken(self):
        r = self.client.get(path=f"{reverse('check-user-name-exists')}?username=hello")
        self.assertFalse(r.json()['taken'])
