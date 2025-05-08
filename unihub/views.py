from django.shortcuts import render, redirect
from django.utils import timezone
from posts.models import Post as RegularPost, tag as Tag
from communities.models import Post as CommunityPost
from events.models import Event
from django.db import models
from itertools import chain
from django.utils.timezone import localtime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def api_hub(request):
    return render(request, "api_hub.html")

def home(request):
    # Handle post creation
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content:  # Only create post if content is not empty
            tag_input = request.POST.get('tags', '') # get tags
            tag_names = [name.strip() for name in tag_input.split(',') if name.strip()] # split tags by comma, remove whitespace
            post = RegularPost.objects.create(
                user=request.user,
                content=content
            )
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name) # Create or get the tag
                post.tags.add(tag_obj) # Add the tag to the post
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Post cannot be empty!')
        return redirect('home')

    # Get regular posts
    regular_posts = RegularPost.objects.select_related('user').all()
    
    # Get community posts (only public ones for non-members)
    if request.user.is_authenticated:
        # Get all communities the user is a member of
        user_communities = request.user.communities.all()
        # Get all public posts and posts from communities the user is a member of
        community_posts = CommunityPost.objects.select_related('author', 'community').filter(
            models.Q(visibility='public') | 
            models.Q(community__in=user_communities)
        )
    else:
        # For non-authenticated users, only show public posts
        community_posts = CommunityPost.objects.select_related('author', 'community').filter(visibility='public')
    
    # Get all events
    events = Event.objects.select_related('community', 'owner').all()
    
    # Create a list of dictionaries containing all content with their type
    all_content = []
    
    # Add regular posts
    for post in regular_posts:
        all_content.append({
            'type': 'regular_post',
            'content': post,
            'timestamp': post.created_at,
            'user': post.user,
            'title': None,
            'community': None
        })
    
    # Add community posts
    for post in community_posts:
        all_content.append({
            'type': 'community_post',
            'content': post,
            'timestamp': post.created_at,
            'user': post.author,
            'title': post.title,
            'community': post.community
        })
    
    # Add events
    for event in events:
        all_content.append({
            'type': 'event',
            'content': event,
            'timestamp': event.start_time,
            'user': event.owner,
            'title': event.title,
            'community': event.community
        })
    
    # Sort all content by timestamp, most recent first
    all_content.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render(request, "home.html", {
        "all_content": all_content,
    })
