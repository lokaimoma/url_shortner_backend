# Created by Kelvin_Clark on 6/19/22, 2:28 PM
from typing import Optional, List

import strawberry
from django.db.models import Q
from django.db.models.aggregates import Sum
from strawberry.types import Info

from apps.linksly.models import URL


@strawberry.type
class Url:
    code: str
    long_url: str
    date_created: str
    status: str
    redirects: int

    def __int__(self, url: URL):
        self.code = url.code
        self.long_url = url.long_url
        self.date_created = url.date_created.__str__()
        self.status = url.status
        self.redirects = url.redirects


@strawberry.type
class Query:
    @strawberry.field
    def total_redirects(self, info: Info) -> Optional[int]:
        return URL.objects.filter(user_id=info.context.user.id).aggregate(Sum('redirects')).get('redirects_sum', None)

    @strawberry.field
    def total_links(self, info: Info) -> int:
        return URL.objects.filter(user_id=info.context.user.id).count()

    @strawberry.field
    def top_links(self, info: Info) -> List[Url]:
        return [Url(url) for url in URL.objects.filter(user_id=info.context.user.id).order_by('-redirects')[0:6]]

    @strawberry.field
    def total_passive_links(self, info: Info) -> int:
        return URL.objects.filter(Q(user_id=info.context.user.id) & Q(status=URL.status_choices[1][0])).count()

    @strawberry.field
    def total_active_links(self, info: Info) -> int:
        return URL.objects.filter(Q(user_id=info.context.user.id) & Q(status=URL.status_choices[0][0])).count()
