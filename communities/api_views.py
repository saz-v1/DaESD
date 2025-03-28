from .serializers import CommunitySerializer, MembershipSerializer, PostSerializer, CommentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Community, Membership, Post, Comment

# DRF generic view to handle listing all Communities and creating a new Community (GET and POST)
class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAdminUser]

# DRF generic view to handle retrieving, updating, and deleting a single Community (GET, PUT, PATCH, DELETE)
class CommunityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAdminUser]

# Membership (same as above comments)
class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAdminUser]

class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAdminUser]

# Post (same as above comments)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

# Comment (same as above comments)
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

