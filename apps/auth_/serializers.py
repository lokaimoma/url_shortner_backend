# Created by Kelvin_Clark on 4/23/22, 2:59 PM
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            return ValidationError(_('Email already exists'))
        except ObjectDoesNotExist:
            return value

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            return ValidationError(_('Username already exists'))
        except ObjectDoesNotExist:
            return value

    def create(self, validated_data: dict):
        return User.objects.create_user(username=validated_data.pop('username'),
                                        password=validated_data.pop('password'),
                                        email=validated_data.pop('email'), **validated_data)
