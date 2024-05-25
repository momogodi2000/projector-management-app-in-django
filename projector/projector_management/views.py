from django.shortcuts import render

def home(request):
    context = {}  # You can add context data for your template here
    return render(request, 'index.html', context)  # Update template path based on your structure
