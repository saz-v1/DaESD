from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Each profile is associated with one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile fields
    study_program = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"