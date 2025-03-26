from django.urls import path
from .views import EventListCreateView, EventRetrieveUpdateDestroyView

urlpatterns = [
    # DRF API paths
    path("", EventListCreateView.as_view(), name="events"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-retrieve-update-destroy"),
]