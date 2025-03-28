from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Event
from .serializers import EventSerializer

# Separate all API views to avoid confusion 

# DRF generic view to handle listing all events and creating a new event (GET and POST)
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser] # Only admins can update or delete events in api end point (http://localhost:8000/api/events/)

# DRF generic view to handle retrieving, updating, and deleting a single event (GET, PUT, PATCH, DELETE)
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser] 