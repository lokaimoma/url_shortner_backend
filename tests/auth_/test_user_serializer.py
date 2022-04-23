# Created by Kelvin_Clark on 4/23/22, 3:13 PM
from django.contrib.auth.models import User
from django.test import TestCase

from apps.auth_.serializers import UserSerializer
from tests.factories import UserFactory


class TestUserSerializer(TestCase):

    def test_in_complete_payload(self):
        s = UserSerializer(data={'email': 'hello@mail.com', 'password': 'something'})
        self.assertFalse(s.is_valid())

    def test_email_username_not_exist_complete_payload(self):
        s = UserSerializer(
            data={'email': 'hello@mail.com', 'password': 'something', 'username': 'some_name', 'first_name': 'ok',
                  'last_name': 'yes'}
        )
        self.assertTrue(s.is_valid())

    def test_email_username_exists_complete_payload(self):
        u: User = UserFactory()
        s = UserSerializer(
            data={'email': u.email, 'password': 'some_pass', 'first_name': u.first_name, 'last_name': u.last_name,
                  'username': u.username}
        )
        self.assertFalse(s.is_valid())
