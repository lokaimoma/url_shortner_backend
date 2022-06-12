# Created by Kelvin_Clark on 6/12/22, 5:23 PM
from rest_framework import permissions

from apps.linksly.models import URL


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, URL):
            if obj.user == request.user:
                return True
        return False
