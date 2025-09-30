from rest_framework import serializers
from .models import Bus, TimeSlot, Registration, LiveLocation, User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id","username","first_name","last_name","email")

class BusSerializer(serializers.ModelSerializer):
    class Meta: model = Bus; fields = "__all__"

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta: model = TimeSlot; fields = "__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta: model = Registration; fields = "__all__"

class LiveLocationSerializer(serializers.ModelSerializer):
    class Meta: model = LiveLocation; fields = "__all__"
