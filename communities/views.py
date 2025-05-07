from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

from .models import Community, Membership, Post, Comment
from .forms import CommunityForm, PostForm, CommentForm

def community_list(request):
    communities = Community.objects.annotate(member_count=Count('members')).order_by('-member_count')
    
    user_created_communities = []
    user_admin_communities = []
    
    if request.user.is_authenticated:
        # Get communities created by user
        user_created_communities = Community.objects.filter(creator=request.user)
        
        # Get communities where user is an admin but not creator
        admin_memberships = Membership.objects.filter(
            user=request.user, 
            role='admin'
        ).exclude(community__creator=request.user)
        
        user_admin_communities = [m.community for m in admin_memberships]
    
    return render(request, 'communities/community_list.html', {
        'communities': communities,
        'user_created_communities': user_created_communities,
        'user_admin_communities': user_admin_communities
    })

def community_detail(request, slug):
    community = get_object_or_404(Community, slug=slug)
    is_member = request.user.is_authenticated and community.members.filter(id=request.user.id).exists()

    # Get posts based on visibility
    if is_member:
        # Members can see all posts
        posts = community.posts.all()
    else:
        # Non-members can only see public posts
        posts = community.posts.filter(visibility='public')

    # Filter events based on ?filter=upcoming or ?filter=past
    filter_type = request.GET.get('filter', 'upcoming')
    if filter_type == 'past':
        events = community.events.filter(start_time__lt=timezone.now()).order_by('-start_time')
    else:
        events = community.events.filter(start_time__gte=timezone.now()).order_by('start_time')

    if request.user.is_authenticated:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            user_role = membership.role
        except Membership.DoesNotExist:
            user_role = None
    else:
        user_role = None
    
    return render(request, 'communities/community_detail.html', {
        'community': community,
        'posts': posts,
        'is_member': is_member,
        'user_role': user_role,
        'events': events,
        'filter_type': filter_type,
    })

@login_required
def create_community(request):
    # Debug information
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User ID: {request.user.id}")
    print(f"Username: {request.user.username}")
    
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            
            # Make creator an admin member
            Membership.objects.create(
                user=request.user,
                community=community,
                role='admin'
            )
            
            messages.success(request, 'Community created successfully!')
            return redirect('community_detail', slug=community.slug)
    else:
        form = CommunityForm()
    
    return render(request, 'communities/community_form.html', {'form': form})

@login_required
def edit_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if user is admin, creator, or staff
    is_authorized = False
    
    # Creator can always edit
    if request.user == community.creator:
        is_authorized = True
    # Staff can always edit
    elif request.user.is_staff:
        is_authorized = True
    # Admin member can edit
    else:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role == 'admin':
                is_authorized = True
        except Membership.DoesNotExist:
            pass
    
    if not is_authorized:
        return HttpResponseForbidden("You don't have permission to edit this community")
    
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, 'Community updated successfully!')
            return redirect('community_detail', slug=community.slug)
    else:
        form = CommunityForm(instance=community)
    
    return render(request, 'communities/community_form.html', {
        'form': form,
        'community': community,
        'edit_mode': True
    })

@login_required
def delete_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if user is creator, staff, or admin
    is_authorized = False
    if request.user == community.creator or request.user.is_staff:
        is_authorized = True
    else:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role == 'admin':
                is_authorized = True
        except Membership.DoesNotExist:
            pass
    
    if not is_authorized:
        return HttpResponseForbidden("You don't have permission to delete this community")
    
    if request.method == 'POST':
        community.delete()
        messages.success(request, 'Community deleted successfully!')
        return redirect('community_list')
    
    return render(request, 'communities/community_confirm_delete.html', {'community': community})

@login_required
def join_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if already a member
    if Membership.objects.filter(user=request.user, community=community).exists():
        messages.info(request, 'You are already a member of this community.')
    else:
        Membership.objects.create(
            user=request.user,
            community=community,
            role='member'
        )
        messages.success(request, f'You have joined {community.name}!')
    
    return redirect('community_detail', slug=community.slug)

@login_required
def leave_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    try:
        membership = Membership.objects.get(user=request.user, community=community)
        
        # Don't let the creator leave their own community
        if community.creator == request.user:
            messages.error(request, "As the creator, you cannot leave your own community. You may delete it instead.")
            return redirect('community_detail', slug=community.slug)
            
        membership.delete()
        messages.success(request, f'You have left {community.name}.')
    except Membership.DoesNotExist:
        messages.info(request, 'You are not a member of this community.')
    
    return redirect('community_list')

@login_required
def create_post(request, community_slug):
    community = get_object_or_404(Community, slug=community_slug)
    
    # Check if user is a member
    if not community.members.filter(id=request.user.id).exists():
        return HttpResponseForbidden("You must be a member to post in this community")
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('community_detail', slug=community_slug)
    else:
        form = PostForm()
    
    return render(request, 'communities/post_form.html', {
        'form': form,
        'community': community
    })

def post_detail(request, community_slug, post_id):
    community = get_object_or_404(Community, slug=community_slug)
    post = get_object_or_404(Post, id=post_id, community=community)
    
    # Check if user can view the post
    is_member = request.user.is_authenticated and community.members.filter(id=request.user.id).exists()
    if not is_member and post.visibility == 'members_only':
        return HttpResponseForbidden("This post is only visible to community members")
    
    comments = post.comments.all()
    
    # Comment form for logged in users
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('post_detail', community_slug=community_slug, post_id=post_id)
        else:
            form = CommentForm()
    else:
        form = None
    
    return render(request, 'communities/post_detail.html', {
        'community': community,
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def edit_post(request, community_slug, post_id):
    community = get_object_or_404(Community, slug=community_slug)
    post = get_object_or_404(Post, id=post_id, community=community)
    
    # Check if user is the author or has admin/moderator role
    if request.user != post.author:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You don't have permission to edit this post")
        except Membership.DoesNotExist:
            return HttpResponseForbidden("You don't have permission to edit this post")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', community_slug=community_slug, post_id=post_id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'communities/post_form.html', {
        'form': form,
        'community': community,
        'post': post,
        'edit_mode': True
    })

@login_required
def delete_post(request, community_slug, post_id):
    community = get_object_or_404(Community, slug=community_slug)
    post = get_object_or_404(Post, id=post_id, community=community)
    
    # Check if user is the author or has admin/moderator role
    if request.user != post.author:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You don't have permission to delete this post")
        except Membership.DoesNotExist:
            return HttpResponseForbidden("You don't have permission to delete this post")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community_detail', slug=community_slug)
    
    return render(request, 'communities/post_confirm_delete.html', {
        'community': community,
        'post': post
    })

@login_required
def manage_members(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if user is admin, creator or staff
    is_authorized = False
    if request.user == community.creator or request.user.is_staff:
        is_authorized = True
    else:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role == 'admin':
                is_authorized = True
        except Membership.DoesNotExist:
            pass
    
    if not is_authorized:
        return HttpResponseForbidden("You don't have permission to manage members")
    
    memberships = Membership.objects.filter(community=community).order_by('role', 'user__username')
    
    # Add context data for creator and staff
    context = {
        'community': community,
        'memberships': memberships,
        'creator': community.creator
    }
    
    return render(request, 'communities/manage_members.html', context)

@login_required
def change_member_role(request, slug, user_id, role):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if user is admin
    try:
        admin_membership = Membership.objects.get(user=request.user, community=community)
        if admin_membership.role != 'admin':
            return HttpResponseForbidden("You don't have permission to change member roles")
    except Membership.DoesNotExist:
        return HttpResponseForbidden("You don't have permission to change member roles")
    
    # Don't allow changing the role of the creator
    if community.creator.id == int(user_id):
        messages.error(request, "You cannot change the role of the community creator")
        return redirect('manage_members', slug=slug)
    
    # Update the role
    membership = get_object_or_404(Membership, user__id=user_id, community=community)
    membership.role = role
    membership.save()
    
    messages.success(request, f"Member's role updated to {role}")
    return redirect('manage_members', slug=slug)

@login_required
def remove_member(request, slug, user_id):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if user is admin, creator, or staff
    is_authorized = False
    if request.user == community.creator or request.user.is_staff:
        is_authorized = True
    else:
        try:
            membership = Membership.objects.get(user=request.user, community=community)
            if membership.role == 'admin':
                is_authorized = True
        except Membership.DoesNotExist:
            pass
    
    if not is_authorized:
        return HttpResponseForbidden("You don't have permission to remove members")
    
    # Don't allow removing the creator
    if community.creator.id == int(user_id):
        messages.error(request, "You cannot remove the community creator")
        return redirect('manage_members', slug=slug)
    
    # Remove the member
    membership = get_object_or_404(Membership, user__id=user_id, community=community)
    membership.delete()
    
    messages.success(request, "Member has been removed from the community")
    return redirect('manage_members', slug=slug) 