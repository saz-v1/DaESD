from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

# Event model follows ERD diagram
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    virtual_link = models.URLField(blank=True)
    community = models.ForeignKey("communities.Community", on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=100, blank=True)
    is_virtual = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # Added owner field to link to creators user model
    
    # New fields
    max_capacity = models.PositiveIntegerField(default=0, help_text="Put 0 for unlimited capacity")
    required_materials = models.TextField(blank=True, help_text="List of materials participants need to bring")
    requires_registration = models.BooleanField(default=False)
    registered_users = models.ManyToManyField(User, through='EventRegistration', related_name='registered_events')
    
    # Orders events by start time
    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        if self.max_capacity == 0:
            return False
        return self.registered_users.count() >= self.max_capacity

class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ['event', 'user']
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"