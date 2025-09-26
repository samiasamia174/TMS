from django.urls import path
from .views_api import BusLocationDetail, BusLocationUpdate
from . import views

urlpatterns = [
    path('api/location/<int:bus_id>/', BusLocationDetail.as_view(), name='api-bus-location'),
    path('api/location/update/', BusLocationUpdate.as_view(), name='api-location-update'),
    path('map/<int:bus_id>/', views.map_view, name='tracking-map'),
]
