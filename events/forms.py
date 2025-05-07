from django import forms
from .models import Event, EventRegistration

# Class used to inherit from Django's ModelForm and to exclude fields and add widgets
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner', 'community', 'registered_users']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'required_materials': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'List materials needed, one per line'}),
            'max_capacity': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
        }

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = []  # No fields to display, just handles the registration action