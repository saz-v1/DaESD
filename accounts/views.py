from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileForm
from communities.models import Membership
from events.models import Event
from django.utils import timezone
from .models import Profile
from django.contrib import messages
import os

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def profile_view(request):
    user = request.user
    # Profile is separate from the User model so it may not exist yet so we use get or create
    profile, created = Profile.objects.get_or_create(user=user)

    # User's communities and count
    memberships = Membership.objects.filter(user=user).select_related("community")
    my_communities = [m.community for m in memberships]
    community_count = len(my_communities)

    # Events from those communities
    upcoming_events = Event.objects.filter(community__in=my_communities, start_time__gte=timezone.now()).order_by("start_time")
    past_events = Event.objects.filter(community__in=my_communities, start_time__lt=timezone.now()).order_by("-start_time")

    # Dumping all the data inside context to send to the template
    context = {
        "user": user,
        "my_communities": my_communities,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "profile": profile,
        "community_count": community_count,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Update profile
            profile = form.save(commit=False)
            profile.save()
            
            # Update user
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def remove_profile_picture(request):
    if request.method == 'POST':
        profile = request.user.profile
        if profile.profile_picture:
            try:
                # Delete the actual file
                profile.profile_picture.delete(save=False)  # This deletes the file
                # Clear the field
                profile.profile_picture = None
                profile.save()
                messages.success(request, 'Profile picture removed successfully.')
            except Exception as e:
                messages.error(request, f'Error removing profile picture: {str(e)}')
        
        return redirect('accounts:edit_profile')
    return redirect('accounts:edit_profile')