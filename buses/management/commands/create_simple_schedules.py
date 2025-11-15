from django.core.management.base import BaseCommand
from buses.models import Bus, Route, Schedule
from django.utils import timezone
from datetime import datetime, timedelta, time

class Command(BaseCommand):
    help = 'Create simple schedules for testing'

    def handle(self, *args, **options):
        buses = Bus.objects.all()
        routes = Route.objects.all()
        
        if not buses or not routes:
            self.stdout.write(
                self.style.ERROR('Need buses and routes. Run add_dhaka_routes first.')
            )
            return

        today = timezone.now().date()
        schedules_created = 0

        # Create 2 schedules for each bus-route combination
        for bus in buses:
            for route in routes:
                # Create morning schedule (8:00 AM)
                schedule1, created1 = Schedule.objects.get_or_create(
                    bus=bus,
                    route=route,
                    date=today,
                    departure_time=time(8, 0),
                    defaults={
                        'arrival_time': time(8, 30),
                        'available_seats': bus.capacity,
                        'is_active': True
                    }
                )
                
                if created1:
                    schedules_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {bus.bus_name} -> {route.route_name} at 8:00 AM')
                    )

                # Create afternoon schedule (2:00 PM)
                schedule2, created2 = Schedule.objects.get_or_create(
                    bus=bus,
                    route=route,
                    date=today,
                    departure_time=time(14, 0),
                    defaults={
                        'arrival_time': time(14, 30),
                        'available_seats': bus.capacity,
                        'is_active': True
                    }
                )
                
                if created2:
                    schedules_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {bus.bus_name} -> {route.route_name} at 2:00 PM')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {schedules_created} schedules!')
        )
