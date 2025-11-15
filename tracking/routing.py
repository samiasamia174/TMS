# tracking/routing.py - পুরো file replace করুন

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # General tracking - all buses
    re_path(r'ws/tracking/$', consumers.TrackingConsumer.as_asgi()),

    # Specific bus tracking
    re_path(r'ws/tracking/bus/(?P<bus_id>\w+)/$', consumers.TrackingConsumer.as_asgi()),
]