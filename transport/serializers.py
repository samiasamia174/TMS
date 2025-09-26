from rest_framework import serializers
from .models import Route, Bus, Registration
from django.contrib.auth import get_user_model

User = get_user_model()

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'name', 'start_point', 'end_point']

class BusSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), write_only=True, source='route'
    )

    class Meta:
        model = Bus
        fields = ['id', 'number', 'route', 'route_id', 'capacity', 'driver_name', 'time_slot', 'driver_photo']

class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False, source='user'
    )
    bus = BusSerializer(read_only=True)
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(), write_only=True, source='bus'
    )

    class Meta:
        model = Registration
        fields = ['id', 'user', 'user_id', 'bus', 'bus_id', 'date', 'seat_no']
