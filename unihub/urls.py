"""
URL configuration for unihub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from .views import api_hub, home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Core app and API
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # Use the home view directly
    path("api/", api_hub, name="api-hub"),  
    # Events app and API
    path("events/", include("events.urls")),  
    path("api/events/", include("events.api_urls")),
    # Communities app and API
    path("communities/", include("communities.urls")),  
    path("api/communities/", include("communities.api_urls")),
    # Accounts app and API
    path("accounts/", include("accounts.urls")),  
    path("posts/", include("posts.urls")),
]

# Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)