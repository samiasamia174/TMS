from django.urls import path
from . import views

app_name = 'buses'  # optional; if used, reverse as 'buses:bus_schedule'

urlpatterns = [
    path('schedule/', views.bus_schedule, name='bus_schedule'),
]