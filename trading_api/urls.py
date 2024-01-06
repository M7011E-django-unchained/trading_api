"""
URL configuration for trading_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib.auth.models import User
from trading_api import settings
from django.apps import apps

from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)

# register all models
app = apps.get_app_config('website')
for model_name, model in app.models.items():
    admin_site.register(model)


urlpatterns = [
    path("admin/", admin_site.urls),
    path("debugAdmin/", admin.site.urls),
    path("api/1/", include("website.urls")),
    path("user/", include("users.urls")),
    path('', include('main.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # ... other URL patterns ...
    ]
