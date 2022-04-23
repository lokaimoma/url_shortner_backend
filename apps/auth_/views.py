from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(['GET'])
def check_username_already_taken(request: Request, *args, **kwargs):
    try:
        username: str = request.query_params['username']
        username = username.strip()
        if username == '':
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Username can\'t be empty'})
        flag = True
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            flag = False
        return Response(data={'taken': flag})
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'A query param of key username is expected'})
