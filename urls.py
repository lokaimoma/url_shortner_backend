from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth_ import views as auth_views
from apps.linksly import views as linksly_views

router = routers.DefaultRouter()
router.register(prefix='urls', viewset=linksly_views.URLViewSet, basename='url')

urlpatterns = [
    path('<str:code>/', linksly_views.handle_redirect, name='handle_redirects'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/check-username-exists/', auth_views.check_username_already_taken, name='check-user-name-exists'),
    path('api/login/', auth_views.login_user, name='login'),
    path('api/register/', auth_views.RegisterUserView.as_view(), name='register-user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
