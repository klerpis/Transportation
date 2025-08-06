"""
URL configuration for aktc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from aktcUI.admin import aktc_admin_site
from django.urls import path, re_path, include
from . import views
from .views import FrontendAppView
from aktc.admin import aktc_admin_site, board_room
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('board/', board_room.urls),
    path('admin/', aktc_admin_site.urls),
    # path('confirmpass/', views.confirm_passenger_arrival, name='confirmpass'),

    path('api/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('aktcUI.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('feedbacksystem.urls')),
    path('api/', include('setupsystem.urls')),
    # path('', include('aktcUI.urls')),
    # path('api/', include('booking.urls')),
    # path('api/cusers/', include('cusers.urls')),

    # admin specific Api's
    path('select-depature/', views.get_departure_dates_choices,
         name='selectdeparture'),

    # *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    re_path(r'^.*$', FrontendAppView.as_view(),
            name='frontend'),  # catch-all for React
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    