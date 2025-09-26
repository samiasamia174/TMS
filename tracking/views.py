from django.shortcuts import render

# Create your views here.
# tracking/views.py
from django.shortcuts import render

def map_view(request, bus_id):
    # your code here
    return render(request, 'tracking/map.html', {'bus_id': bus_id})
