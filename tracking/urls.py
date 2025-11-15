# tracking/urls.py - পুরো file replace করুন

from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # User facing views
    path('', views.live_tracking, name='live_tracking'),
    path('live-map/', views.live_map, name='live_map'),
    path('bus/<int:bus_id>/', views.bus_tracking_detail, name='bus_tracking_detail'),
    path('notifications/', views.notifications_list, name='notifications_list'),

    # API endpoints
    path('api/bus/<int:bus_id>/location/', views.get_bus_location_api, name='get_bus_location_api'),
    path('api/update-location/', views.UpdateLocationView.as_view(), name='api_update_location'),

    # Authority management
    path('manage/', views.manage_tracking, name='manage_tracking'),
    path('manage/update-location/', views.update_location, name='update_location'),
    path('manage/update-status/', views.update_status, name='update_status'),
    path('manage/update-status/<int:bus_id>/', views.update_status, name='update_status_bus'),
    path('manage/create-notification/', views.create_notification, name='create_notification'),
]