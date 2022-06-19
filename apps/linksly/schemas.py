# Created by Kelvin_Clark on 6/19/22, 2:28 PM
from typing import List

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


@strawberry.type
class Query:
    @strawberry.field
    def total_redirects(self, info: Info) -> int:
        result = URL.objects.filter(user_id=info.context['request'].user.id).aggregate(Sum('redirects'))
        return result.get('redirects__sum', 0)

    @strawberry.field
    def total_links(self, info: Info) -> int:
        return URL.objects.filter(user_id=info.context['request'].user.id).count()

    @strawberry.field
    def top_links(self, info: Info) -> List[Url]:
        return [Url(code=url.code, long_url=url.long_url, date_created=url.date_created,
                    status=url.date_created.__str__(), redirects=url.redirects) for url in
                URL.objects.filter(Q(user_id=info.context['request'].user.id) &
                                   Q(redirects__gt=5)).order_by('-redirects')[0:6]
                ]

    @strawberry.field
    def total_passive_links(self, info: Info) -> int:
        return URL.objects.filter(
            Q(user_id=info.context['request'].user.id) & Q(status=URL.status_choices[1][0])).count()

    @strawberry.field
    def total_active_links(self, info: Info) -> int:
        return URL.objects.filter(
            Q(user_id=info.context['request'].user.id) & Q(status=URL.status_choices[0][0])).count()
