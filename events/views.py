from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EventForm
from django.urls import reverse_lazy
from django.utils import timezone

# DRF generic view to handle listing all events and creating a new event (GET and POST)
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# DRF generic view to handle retrieving, updating, and deleting a single event (GET, PUT, PATCH, DELETE)
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Django view to render a list of events
# Also includes a filter to show only past or upcoming events
def event_list_view(request):
    filter_type = request.GET.get('filter', 'upcoming')

    if filter_type == 'past':
        events = Event.objects.filter(start_time__lt=timezone.now()).order_by('-start_time')
    else:
        events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')

    return render(request, "events/events.html", {
        "events": events,
        "filter_type": filter_type,
    })

# Django view to render a single event
def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/event_detail.html", {"event": event})

# Django view to create a new event
class EventCreateView(CreateView):
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
class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EventForm
    def get_success_url(self):
        return reverse_lazy('community_detail', kwargs={'slug': self.object.community.slug})

# Django view to delete an existing event
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('community_detail', kwargs={'slug': self.object.community.slug})