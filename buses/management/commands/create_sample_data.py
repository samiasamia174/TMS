from django.core.management.base import BaseCommand
from buses.models import Route, Bus, Schedule
from datetime import time

class Command(BaseCommand):
    help = 'Create sample data for booking system using correct field names'
    
    def handle(self, *args, **options):
        # First, let's see what data already exists
        existing_routes = Route.objects.count()
        existing_buses = Bus.objects.count()
        existing_schedules = Schedule.objects.count()
        
        self.stdout.write(f'Existing data - Routes: {existing_routes}, Buses: {existing_buses}, Schedules: {existing_schedules}')
        
        # Show existing buses with correct field names
        self.stdout.write('Existing buses:')
        for bus in Bus.objects.all():
            bus_name = getattr(bus, 'bus_name', 'N/A')
            self.stdout.write(f'  - {bus.bus_number} ({bus_name}) - Capacity: {bus.capacity}')
        
        # Only create routes if none exist
        if existing_routes == 0:
            routes_data = [
                {
                    'route_name': 'Campus to Farmgate', 
                    'start_point': 'UAP Campus', 
                    'end_point': 'Farmgate', 
                    'distance': 8.5, 
                    'fare': 30.00, 
                    'estimated_time': 30.0,
                    'is_active': True
                },
                {
                    'route_name': 'Campus to Dhanmondi', 
                    'start_point': 'UAP Campus', 
                    'end_point': 'Dhanmondi', 
                    'distance': 6.2, 
                    'fare': 25.00, 
                    'estimated_time': 25.0,
                    'is_active': True
                },
                {
                    'route_name': 'Campus to Mirpur', 
                    'start_point': 'UAP Campus', 
                    'end_point': 'Mirpur', 
                    'distance': 12.0, 
                    'fare': 40.00, 
                    'estimated_time': 45.0,
                    'is_active': True
                },
            ]
            
            for route_data in routes_data:
                route = Route.objects.create(**route_data)
                self.stdout.write(self.style.SUCCESS(f'Created route: {route.route_name}'))
        
        # Create schedules using existing buses
        if existing_schedules == 0 and Route.objects.exists() and Bus.objects.exists():
            routes = list(Route.objects.all())
            buses = list(Bus.objects.all())
            
            # Create schedules for each route with available buses
            schedules_data = []
            for i, route in enumerate(routes):
                if i < len(buses):
                    schedules_data.append({
                        'bus': buses[i],
                        'route': route,
                        'departure_time': time(8 + i, 0),  # 8:00, 9:00, 10:00
                        'arrival_time': time(8 + i, 30),   # 8:30, 9:30, 10:30  
                        'available_seats': buses[i].capacity
                    })
            
            for schedule_data in schedules_data:
                schedule = Schedule.objects.create(**schedule_data)
                bus_name = getattr(schedule.bus, 'bus_name', 'N/A')
                self.stdout.write(self.style.SUCCESS(f'Created schedule: {schedule.bus.bus_number} - {schedule.route.route_name}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))
