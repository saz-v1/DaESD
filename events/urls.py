from django.urls import path
from .views import event_list_view, event_detail_view, EventCreateView, EventDeleteView, EventUpdateView, event_register

urlpatterns = [
    # List and detail paths
    path('', event_list_view, name='event-list'),
    path('<int:pk>/', event_detail_view, name='event-detail'), 
    # Create path
    path('create/', EventCreateView.as_view(), name='event-create'), 
    # Edit and delete paths
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    # Registration path
    path('events/<int:pk>/register/', event_register, name='event-register'),
]