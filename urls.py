from django.contrib import admin
from django.urls import path

from apps.auth_ import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/check-username-exists/', auth_views.check_username_already_taken, name='check-user-name-exists'),
    path('api/register/', auth_views.RegisterUserView.as_view(), name='register-user'),
]
