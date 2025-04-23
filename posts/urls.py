from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts_home, name='posts_home'),  
]