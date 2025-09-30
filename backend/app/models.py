from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)

class Bus(models.Model):
    number = models.CharField(max_length=20, unique=True)
    route = models.CharField(max_length=255)
    capacity = models.IntegerField(default=40)
    active = models.BooleanField(default=True)
    def __str__(self): return f"{self.number} - {self.route}"

class TimeSlot(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="timeslots")
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    def __str__(self): return f"{self.bus.number} {self.departure_time}"

class Registration(models.Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id = None

    user = models.ForeignKey("app.User", on_delete=models.CASCADE, related_name="registrations")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_ref = models.CharField(max_length=255, null=True, blank=True)
    class Meta: unique_together = ("user","bus","timeslot")

class LiveLocation(models.Model):
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE, related_name="location")
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
