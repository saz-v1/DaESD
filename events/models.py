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
    # Orders events by start time
    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.title