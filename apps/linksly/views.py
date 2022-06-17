from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.linksly.models import URL
from apps.linksly.permissions import IsOwner
from apps.linksly.serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(user_id=user.id)


@api_view(['GET'])
def handle_redirect(request: Request, *args, **kwargs):
    try:
        url = URL.objects.get(pk=kwargs['code'], status=URL.status_choices[0][0])
        url.redirects = url.redirects + 1
        url.save()
        response = Response(status=status.HTTP_307_TEMPORARY_REDIRECT, data={})
        response['Location'] = url.long_url
        return response
    except ObjectDoesNotExist:
        return render(request, 'linksly/404.html',status=status.HTTP_400_BAD_REQUEST)
