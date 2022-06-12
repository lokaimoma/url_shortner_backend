from rest_framework import viewsets, permissions
from rest_framework import decorators
from rest_framework.request import Request

from apps.linksly.models import URL
from apps.linksly.permissions import IsOwner
from apps.linksly.serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(user_id=user.id)


@decorators.api_view(['PATCH'])
@decorators.permission_classes([IsOwner])
def change_url_status(request: Request, *args, **kwargs):
    pass
