# Created by Kelvin_Clark on 4/21/22, 5:55 PM
import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from apps.linksly.models import URL
from tests import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: faker.unique.name())
    email = factory.LazyAttribute(lambda _: faker.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    password = factory.LazyAttribute(lambda _: make_password('hello'))


class URLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = URL
        django_get_or_create = ('code',)

    user = factory.SubFactory(UserFactory)
    code = factory.LazyAttribute(lambda _: faker.unique.pystr()[:5])
    long_url = factory.LazyAttribute(lambda _: faker.domain_name())
