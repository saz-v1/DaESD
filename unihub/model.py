# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Extended user model with additional fields for student profiles"""
    study_program = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username

class Community(models.Model):
    """Model for interest-based communities"""
    CATEGORY_CHOICES = [
        ('academic_subject', 'Academic Subject'),
        ('study_group', 'Study Group'),
        ('research', 'Research'),
        ('student_organization', 'Student Organization'),
        ('sports_recreation', 'Sports & Recreation'),
        ('arts_culture', 'Arts & Culture'),
        ('technology', 'Technology'),
        ('career_professional', 'Career & Professional'),
        ('volunteering_service', 'Volunteering & Service'),
        ('sustainability_environment', 'Sustainability & Environment'),
        ('wellness_health', 'Wellness & Health'),
        ('diversity_inclusion', 'Diversity & Inclusion'),
        ('hobbies_interests', 'Hobbies & Interests'),
        ('entertainment_leisure', 'Entertainment & Leisure'),
        ('residential', 'Residential'),
        ('international_cultural', 'International & Cultural'),
        ('entrepreneurship', 'Entrepreneurship'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='CommunityMembership', related_name='communities')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Communities"

class CommunityMembership(models.Model):
    """Junction model for user-community membership"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    is_leader = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default='Member')
    
    class Meta:
        unique_together = ('user', 'community')
        
    def __str__(self):
        return f"{self.user.username} - {self.community.name}"

class Event(models.Model):
    """Model for community events"""
    EVENT_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('social', 'Social'),
        ('professional', 'Professional'),
        ('workshop', 'Workshop'),
        ('meeting', 'Meeting'),
        ('conference', 'Conference'),
        ('performance', 'Performance'),
        ('sports', 'Sports'),
        ('service', 'Service'),
        ('cultural', 'Cultural'),
        ('webinar', 'Webinar'),
        ('competition', 'Competition'),
        ('info_session', 'Information Session'),
        ('field_trip', 'Field Trip'),
        ('wellness', 'Wellness'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    virtual_link = models.URLField(blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    is_virtual = models.BooleanField(default=False)
    attendees = models.ManyToManyField(User, through='EventRegistration', related_name='events')
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    """Junction model for user-event registration"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'event')
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Post(models.Model):
    """Model for community posts and updates"""
    title = models.CharField(max_length=100)
    content = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model for comments on posts"""
    content = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('event_invitation', 'Event Invitation'),
        ('event_reminder', 'Event Reminder'),
        ('event_update', 'Event Update'),
        ('event_cancellation', 'Event Cancellation'),
        ('new_community_post', 'New Community Post'),
        ('post_comment', 'Post Comment'),
        ('comment_reply', 'Comment Reply'),
        ('community_join_request', 'Community Join Request'),
        ('community_join_approved', 'Community Join Approved'),
        ('membership_role_change', 'Membership Role Change'),
        ('mentioned_in_post', 'Mentioned in Post'),
        ('mentioned_in_comment', 'Mentioned in Comment'),
        ('welcome_notification', 'Welcome Notification'),
        ('system_announcement', 'System Announcement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    reference_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.content[:30]}..."