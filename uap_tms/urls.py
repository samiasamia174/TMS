from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Import views from buses app
from buses.views import home, route_list, bus_list, booking_view, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main pages - use proper views from buses app that query database
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('buses/', bus_list, name='buses'),
    path('routes/', route_list, name='routes'),
    path('booking/', booking_view, name='booking'),
    
    # Include other app URLs
    path('accounts/', include('accounts.urls')),
    path('', include('buses.urls')),  # For auth URLs
]

# Remove the old hardcoded views
