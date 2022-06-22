from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from strawberry.django.views import GraphQLView

from apps.linksly.models import URL
from apps.linksly.permissions import IsOwner
from apps.linksly.serializers import URLSerializer, UserInfoUpdateSerializer


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
        return render(request, 'linksly/404.html', status=status.HTTP_404_NOT_FOUND)


class LinkslyGraphqlView(GraphQLView):
    def get_context(self, request: Request, response: HttpResponse) -> dict:
        try:
            tk = request.headers['Authorization'].split(" ")[1]
            token = AccessToken(token=tk)
            request.user = User.objects.get(pk=token['user_id'])
        except (TokenError, KeyError, IndexError):
            pass
        return {
            'request': request,
            'response': response
        }


class UpdateUserInfoView(generics.UpdateAPIView):
    serializer_class = UserInfoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
