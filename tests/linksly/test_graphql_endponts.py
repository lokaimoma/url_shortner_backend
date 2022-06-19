# Created by Kelvin_Clark on 6/19/22, 3:17 PM
from django.test import TestCase
from django.urls import reverse

from apps.linksly.models import URL
from tests import factories, get_auth_headers


class TestGraphqlEndpoints(TestCase):
    def setUp(self) -> None:
        self.user = factories.UserFactory()
        self.header = get_auth_headers(username=self.user.username, client=self.client)

    def test_get_total_redirects(self):
        url1: URL = factories.URLFactory()
        url1.redirects = 10
        url1.user = self.user
        url1.save()
        url2: URL = factories.URLFactory()
        url2.redirects = 5
        url2.user = self.user
        url2.save()
        query = """
            query TOTAL_REDIRECTS {
                totalRedirects
            }
        """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOTAL_REDIRECTS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(json['data']['totalRedirects'], 15)

    def test_total_links_no_links(self):
        query = """
                    query TOTAL_LINKS {
                        totalLinks
                    }
                """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOTAL_LINKS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(json['data']['totalLinks'], 0)

    def test_total_links_have_links(self):
        url = factories.URLFactory()
        url.user = self.user
        url.save()
        query = """
                    query TOTAL_LINKS {
                        totalLinks
                    }
                """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOTAL_LINKS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(json['data']['totalLinks'], 1)

    def test_top_links(self):
        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 9
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 8
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 6
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 4
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.save()

        query = """
                            query TOP_LINKS {
                                topLinks{code}
                            }
                        """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOP_LINKS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(len(json['data']['topLinks']), 4)

    def test_total_passive_links(self):
        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.status = URL.status_choices[1][0]
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.status = URL.status_choices[1][0]
        url.save()

        query = """
                                    query TOTAL_PASSIVE_LINKS {
                                        totalPassiveLinks
                                    }
                                """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOTAL_PASSIVE_LINKS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(json['data']['totalPassiveLinks'], 2)

    def test_total_active_links(self):
        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.status = URL.status_choices[1][0]
        url.save()

        url = factories.URLFactory()
        url.user = self.user
        url.redirects = 10
        url.status = URL.status_choices[1][0]
        url.save()

        query = """
                    query TOTAL_ACTIVE_LINKS {
                        totalActiveLinks
                    }
                """
        r = self.client.get(path=reverse('graphql'),
                            data={'query': query, 'operationName': 'TOTAL_ACTIVE_LINKS', 'variables': {}},
                            **self.header
                            )
        json = r.json()
        self.assertNotIn('errors', json)
        self.assertEquals(json['data']['totalActiveLinks'], 2)
