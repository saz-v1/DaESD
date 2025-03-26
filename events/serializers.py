from rest_framework import serializers
from .models import Event

# Grabs event model and serializes data into JSON
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
