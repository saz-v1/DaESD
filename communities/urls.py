from django.urls import path
from . import views

urlpatterns = [
    # Main community listing page showing all available communities
    path('', views.community_list, name='community_list'),
    
    # Form for creating a new community - requires authentication
    path('create/', views.create_community, name='create_community'),
    
    # Community detail view using slug for SEO-friendly URLs
    # The slug is auto-generated from the community name
    path('<slug:slug>/', views.community_detail, name='community_detail'),
    
    # Edit community details - restricted to community admins
    path('<slug:slug>/edit/', views.edit_community, name='edit_community'),
    
    # Delete community with confirmation - restricted to community admins
    path('<slug:slug>/delete/', views.delete_community, name='delete_community'),
    
    # Handles membership actions - join with default 'member' role
    path('<slug:slug>/join/', views.join_community, name='join_community'),
    
    # Leave community - creators cannot leave their own communities
    path('<slug:slug>/leave/', views.leave_community, name='leave_community'),
    
    # Admin page for managing community members and roles
    path('<slug:slug>/members/', views.manage_members, name='manage_members'),
    
    # Change a member's role (member/moderator/admin) - admin only
    path('<slug:slug>/members/<int:user_id>/change-role/<str:role>/', views.change_member_role, name='change_member_role'),
    
    # Remove a member from community - admin only, cannot remove creator
    path('<slug:slug>/members/<int:user_id>/remove/', views.remove_member, name='remove_member'),
    
    # Create a new post in the community - members only
    path('<slug:community_slug>/post/create/', views.create_post, name='create_post'),
    
    # View a specific post and its comments
    path('<slug:community_slug>/post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Edit post - restricted to author or community moderators/admins
    path('<slug:community_slug>/post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    
    # Delete post with confirmation - restricted to author or community moderators/admins
    path('<slug:community_slug>/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
] 