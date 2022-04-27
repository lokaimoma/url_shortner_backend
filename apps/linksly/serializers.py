# Created by Kelvin_Clark on 4/27/22, 2:19 PM
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

    def create(self, validated_data):
        request: Request = self.context.get('request')
        if not request:
            raise Http404
        user = request.user
        while True:
            code = shortuuid.ShortUUID.random(length=5)
            try:
                URL.objects.get(code=code)
            except ObjectDoesNotExist:
                break
        return URL.objects.create(**validated_data, code=code, user_id=user.id)



