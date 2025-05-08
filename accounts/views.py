from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileForm, CustomUserCreationForm
from communities.models import Membership, Community
from events.models import Event
from django.utils import timezone
from .models import Profile
from django.contrib import messages
from django.db.models import Q
import os

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect("accounts:edit_profile")
    else:
        form = CustomUserCreationForm()
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

@login_required
def search_students(request):
    query = request.GET.get('q', '')
    program = request.GET.get('program', '')
    year = request.GET.get('year', '')
    
    # Start with all profiles
    profiles = Profile.objects.select_related('user').all()
    
    if query:
        # Search in username, first name, last name, and bio
        profiles = profiles.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if program:
        profiles = profiles.filter(study_program__icontains=program)
    
    if year:
        profiles = profiles.filter(study_year=year)
    
    # Get unique study programs for filter dropdown
    study_programs = Profile.objects.exclude(study_program__isnull=True).values_list('study_program', flat=True).distinct()
    
    context = {
        'profiles': profiles,
        'query': query,
        'program': program,
        'year': year,
        'study_programs': study_programs,
        'year_choices': Profile.YEAR_CHOICES,
    }
    
    return render(request, 'accounts/search_students.html', context)

def global_search(request):
    query = request.GET.get('q', '').strip()
    student_results = []
    community_results = []
    event_results = []

    if query:
        # Student search (profiles)
        student_results = Profile.objects.select_related('user').filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(study_program__icontains=query)
        )
        # Community search
        community_results = Community.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        # Event search
        event_results = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    context = {
        'query': query,
        'student_results': student_results,
        'community_results': community_results,
        'event_results': event_results,
    }
    return render(request, 'accounts/global_search_results.html', context)