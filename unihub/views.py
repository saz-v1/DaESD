from django.shortcuts import render

def api_hub(request):
    return render(request, "api_hub.html")
