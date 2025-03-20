from django.shortcuts import render

def event_view(request):
    return render(request, 'events/events.html')