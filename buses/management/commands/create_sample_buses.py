from django.core.management.base import BaseCommand
from buses.models import Bus, Route, Schedule
from django.utils import timezone
from datetime import datetime, timedelta, time

class Command(BaseCommand):
    help = 'Create sample buses and schedules'

    def handle(self, *args, **options):
        # Get all routes
        routes = Route.objects.all()
        
        if not routes:
            self.stdout.write(
                self.style.ERROR('No routes found. Please run add_dhaka_routes first.')
            )
            return

        # Create buses
        bus_data = [
            {'bus_number': 'UAP-AC-001', 'bus_name': 'AC Bus - Premium Service', 'capacity': 40},
            {'bus_number': 'UAP-AC-002', 'bus_name': 'AC Bus - Express Service', 'capacity': 40},
            {'bus_number': 'UAP-NAC-001', 'bus_name': 'Non-AC Bus - Regular Service', 'capacity': 50},
            {'bus_number': 'UAP-NAC-002', 'bus_name': 'Non-AC Bus - Standard Service', 'capacity': 50},
            {'bus_number': 'UAP-MINI-001', 'bus_name': 'Mini Bus - Shuttle Service', 'capacity': 25},
            {'bus_number': 'UAP-MINI-002', 'bus_name': 'Mini Bus - Quick Service', 'capacity': 25},
        ]

        buses_created = []
        for bus_info in bus_data:
            bus, created = Bus.objects.get_or_create(
                bus_number=bus_info['bus_number'],
                defaults={
                    'bus_name': bus_info['bus_name'],
                    'capacity': bus_info['capacity'],
                    'is_active': True
                }
            )
            if created:
                buses_created.append(bus)
                self.stdout.write(
                    self.style.SUCCESS(f'Created bus: {bus.bus_name}')
                )

        # Create schedules linking buses to routes with all required fields
        today = timezone.now().date()
        for route in routes:
            for bus in buses_created:
                # Calculate arrival time based on route estimated_time
                estimated_minutes = route.estimated_time
                
                # Create multiple schedules for today and tomorrow
                for day_offset in [0, 1]:  # Today and tomorrow
                    schedule_date = today + timedelta(days=day_offset)
                    
                    # Create 3 schedules per day per bus-route combination
                    departure_times = [time(7, 0), time(11, 0), time(15, 0)]  # 7AM, 11AM, 3PM
                    
                    for departure_time_obj in departure_times:
                        # Calculate arrival time (add estimated minutes to departure time)
                        departure_datetime = datetime.combine(schedule_date, departure_time_obj)
                        arrival_datetime = departure_datetime + timedelta(minutes=estimated_minutes)
                        arrival_time_obj = arrival_datetime.time()
                        
                        schedule, created = Schedule.objects.get_or_create(
                            bus=bus,
                            route=route,
                            date=schedule_date,
                            departure_time=departure_time_obj,
                            defaults={
                                'arrival_time': arrival_time_obj,
                                'available_seats': bus.capacity,
                                'is_active': True
                            }
                        )
                        
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f'Created schedule: {bus.bus_name} -> {route.route_name} on {schedule_date} at {departure_time_obj}')
                            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created all sample buses and schedules!')
        )
