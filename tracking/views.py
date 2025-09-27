from django.shortcuts import render, get_object_or_404
from transport.models import Bus
from django.conf import settings

def map_view(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    context = {'bus': bus, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'tracking/map.html', context)
