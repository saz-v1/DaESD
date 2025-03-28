from django.urls import path, include
from .views import register, profile_view, edit_profile

urlpatterns = [
    path("register/", register, name="register"),  # custom register view
    path("profile/", profile_view, name="profile"),  # custom profile view
    path("", include("django.contrib.auth.urls")),  # built-in login, logout, password reset, etc.
    path('edit/', edit_profile, name='edit-profile'),
]