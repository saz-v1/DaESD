# File: events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventRegistration
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EventForm, EventRegistrationForm
from django.urls import reverse_lazy
from django.utils import timezone
from .mixins import EventPermissionMixin
from django.db.models import Q  # Added for search functionality
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Django view to render a list of events
# Also includes a filter to show only past or upcoming events and search functionality
def event_list_view(request):
    filter_type = request.GET.get('filter', 'upcoming')
    search_query = request.GET.get('search', '')

    # Base query for filtering upcoming or past events
    if filter_type == 'past':
        events = Event.objects.filter(start_time__lt=timezone.now()).order_by('-start_time')
    else:
        events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')

    # Apply search filter if search query is provided
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(location__icontains=search_query) | 
            Q(community__name__icontains=search_query)
        )

    return render(request, "events/events.html", {
        "events": events,
        "filter_type": filter_type,
        "search_query": search_query,
    })

# Django view to render a single event
def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/event_detail.html", {"event": event})

# Django view to create a new event
# EventPermissionMixin - custom mixin to handle permission checks
# Check mixins.py for more details
class EventCreateView(EventPermissionMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    success_url = '/events/'
    form_class = EventForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        community_id = self.request.GET.get('community')
        if community_id:
            form.instance.community_id = community_id
        return super().form_valid(form)
    
# Django view to update an existing event
class EventUpdateView(EventPermissionMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('community_detail', kwargs={'slug': self.object.community.slug})

# Django view to delete an existing event
class EventDeleteView(EventPermissionMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('community_detail', kwargs={'slug': self.object.community.slug})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not event.requires_registration:
        messages.error(request, "This event does not require registration.")
        return redirect('event-detail', pk=pk)
    
    if event.is_full:
        messages.error(request, "This event is full.")
        return redirect('event-detail', pk=pk)
    
    if request.user in event.registered_users.all():
        messages.info(request, "You are already registered for this event.")
        return redirect('event-detail', pk=pk)
    
    if request.method == 'POST':
        registration = EventRegistration.objects.create(
            event=event,
            user=request.user,
            status='confirmed'
        )
        
        # Send confirmation email
        subject = f'Registration Confirmed: {event.title}'
        message = f'''Hello {request.user.username},

Your registration for {event.title} has been confirmed.

Event Details:
Date: {event.start_time.strftime('%B %d, %Y at %I:%M %p')}
Location: {event.location if not event.is_virtual else 'Virtual Event'}
'''

        if event.required_materials:
            message += f'''
Required Materials:
{event.required_materials}
'''

        message += '''
Thank you for registering!
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=True,
        )
        
        messages.success(request, "You have successfully registered for this event!")
        return redirect('event-detail', pk=pk)
    
    return render(request, 'events/event_register.html', {'event': event})
