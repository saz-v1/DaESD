from django.db import models
from django.contrib.auth.models import User

class tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='yasen_form')  # User who created the post
    content = models.TextField()  # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation time
    tags = models.ManyToManyField(tag, blank=True) # many to many relationship with tag
    attachment = models.FileField(upload_to='regular_post_attachments/', null=True, blank=True)
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

class Notification(models.Model):   
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)