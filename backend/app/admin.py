from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Bus, TimeSlot, Registration, LiveLocation, User
from django.contrib.auth.admin import UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Bus)
admin.site.register(TimeSlot)
admin.site.register(Registration)
admin.site.register(LiveLocation)
