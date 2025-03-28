from django.urls import path
from . import api_views

urlpatterns = [
    # DRF API paths

    # Community
    path('', api_views.CommunityListCreateView.as_view(), name='api-community-list-create'),
    path('<int:pk>/', api_views.CommunityRetrieveUpdateDestroyView.as_view(), name='api-community-detail'),

    # Membership
    path('memberships/', api_views.MembershipListCreateView.as_view(), name='api-membership-list-create'),
    path('memberships/<int:pk>/', api_views.MembershipRetrieveUpdateDestroyView.as_view(), name='api-membership-detail'),

    # Post
    path('posts/', api_views.PostListCreateView.as_view(), name='api-post-list-create'),
    path('posts/<int:pk>/', api_views.PostRetrieveUpdateDestroyView.as_view(), name='api-post-detail'),

    # Comment
    path('comments/', api_views.CommentListCreateView.as_view(), name='api-comment-list-create'),
    path('comments/<int:pk>/', api_views.CommentRetrieveUpdateDestroyView.as_view(), name='api-comment-detail'),
]
