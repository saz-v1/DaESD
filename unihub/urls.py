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
from .views import api_home, register, profile_view

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("api/", api_home, name="api-home"),  # API home route
    path("accounts/", include("django.contrib.auth.urls")),  #  Adds login/logout/password reset
    path("register/", register, name="register"),  #  User Registration
    path("profile/", profile_view, name='profile')
    path("", include("events.urls")),  #  Include events app urls
]