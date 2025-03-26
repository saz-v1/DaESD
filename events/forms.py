from django import forms
from .models import Event

# Class used to inherit from Django's ModelForm and to exclude fields and add widgets
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner', 'community'] 
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }