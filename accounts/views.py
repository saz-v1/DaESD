from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileForm
from communities.models import Membership
from events.models import Event
from django.utils import timezone
from .models import Profile

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
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Forms from forms.py file to edit user and profile
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'user_form': user_form,'profile_form': profile_form})