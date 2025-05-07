from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts_home, name='posts_home'),  
    path('posts/', views.mark_notifications_read, name='mark_notifications_read'),
    path('posts/<int:post_id>/comment/', views.post_comment, name='post_comment'),
]