from django.urls import path
from . import views

app_name = 'buses'  # This is important for namespace

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule/', views.bus_schedule, name='bus_schedule'),  # Add this line
    # Add other URL patterns as needed
]