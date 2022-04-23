# Created by Kelvin_Clark on 4/23/22, 3:25 PM
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from tests import faker
from tests.factories import UserFactory


class TestRegisterUser(TestCase):
    def test_register_user_no_duplicate(self):
        payload = {'first_name': faker.first_name(), 'last_name': faker.last_name(), 'email': faker.email(),
                   'password': 'hello', 'username': faker.first_name()}
        r = self.client.post(path=reverse('register-user'), data=payload)
        self.assertEquals(r.status_code, status.HTTP_201_CREATED)
        u = User.objects.get(email=payload.get('email'))
        self.assertEquals(u.first_name, payload.get('first_name'))
        self.assertEquals(u.last_name, payload.get('last_name'))
        self.assertEquals(u.username, payload.get('username'))

    def test_register_user_duplicate(self):
        u: User = UserFactory()
        payload = {'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email,
                   'password': 'hello', 'username': u.username}
        r = self.client.post(path=reverse('register-user'), data=payload)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
