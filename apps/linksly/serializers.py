# Created by Kelvin_Clark on 4/27/22, 2:19 PM
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers
from rest_framework.request import Request
import shortuuid

from apps.linksly.models import URL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        read_only_fields = ['date_created', 'code']
        exclude = ['user']

    def create(self, validated_data: dict):
        request: Request = self.context.get('request')
        if not request:
            raise Http404
        user = request.user
        while True:
            code = shortuuid.ShortUUID().random(length=5)
            try:
                URL.objects.get(code=code)
            except ObjectDoesNotExist:
                break
        return URL.objects.create(**validated_data, code=code, user_id=user.id)

    def update(self, instance: URL, validated_data: dict):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def validate_email(self, value: str):
        users = User.objects.filter(email__iexact=value)
        if len(users) > 0:
            raise serializers.ValidationError('Email is already taken')
        return value
