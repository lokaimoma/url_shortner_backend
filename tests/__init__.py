# Created by Kelvin_Clark on 4/21/22, 5:46 PM
from django.test import Client
import faker as f

faker = f.Faker()


def get_auth_headers(username: str, client: Client, password: str = 'hello') -> dict:
    from django.urls import reverse
    r = client.post(path=reverse('token_obtain_pair'), data={'username': username, 'password': password})
    json = r.json()
    auth_header = {'HTTP_AUTHORIZATION': f'Bearer {json["access"]}'}
    return auth_header
