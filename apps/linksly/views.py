from rest_framework import viewsets, permissions

from apps.linksly.models import URL
from apps.linksly.permissions import IsOwner
from apps.linksly.serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(user_id=user.id)
