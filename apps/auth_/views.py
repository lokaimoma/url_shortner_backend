from typing import Union

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_ import serializers


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


class RegisterUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


@api_view(['POST'])
def login_user(request: Request, *args, **kwargs):
    try:
        username = request.data['username']
        password = request.data['password']
        user: Union[User, None] = authenticate(username=username, password=password)
        if not user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'No account found with the provided credentials', 'status': status.HTTP_400_BAD_REQUEST}
            )
        tokens = RefreshToken.for_user(user=user)
        return Response(
            data={
                'username': username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'access': str(tokens.access_token),
                'refresh': str(tokens)
            }
        )
    except KeyError:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'username': 'This field is required',
                'password': 'This field is required',
                'status': status.HTTP_400_BAD_REQUEST
            }
        )
