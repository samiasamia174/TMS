from django.core.management.base import BaseCommand
from buses.models import Route, Bus, Schedule
from datetime import time
from datetime import date, datetime, timedelta

class Command(BaseCommand):
    help = 'Add realistic Dhaka city bus routes to UAP Campus'
    
    def handle(self, *args, **options):
        # Clear existing sample data first (optional - comment out if you want to keep existing)
        # Schedule.objects.all().delete()
        # Route.objects.all().delete()
        
        self.stdout.write('🚌 Adding Dhaka City Bus Routes to UAP Campus...')
        
        # Dhaka City Routes Data
        dhaka_routes = [
            {
                'route_name': 'Farmgate to UAP Campus',
                'start_point': 'Farmgate',
                'end_point': 'UAP Campus, Green Road',
                'distance': 3.5,
                'fare': 25.00,
                'estimated_time': 15.0,
            },
            {
                'route_name': 'Dhanmondi 27 to UAP Campus',
                'start_point': 'Dhanmondi 27',
                'end_point': 'UAP Campus, Green Road', 
                'distance': 4.2,
                'fare': 20.00,
                'estimated_time': 20.0,
            },
            {
                'route_name': 'Mirpur 10 to UAP Campus',
                'start_point': 'Mirpur 10',
                'end_point': 'UAP Campus, Green Road',
                'distance': 8.5,
                'fare': 35.00,
                'estimated_time': 35.0,
            },
            {
                'route_name': 'Mohammadpur to UAP Campus',
                'start_point': 'Mohammadpur Bus Stand',
                'end_point': 'UAP Campus, Green Road',
                'distance': 5.0,
                'fare': 25.00,
                'estimated_time': 25.0,
            },
            {
                'route_name': 'Uttara to UAP Campus',
                'start_point': 'Uttara Sector 1',
                'end_point': 'UAP Campus, Green Road',
                'distance': 18.0,
                'fare': 60.00,
                'estimated_time': 60.0,
            },
            {
                'route_name': 'Gulshan 1 to UAP Campus',
                'start_point': 'Gulshan 1 Circle',
                'end_point': 'UAP Campus, Green Road',
                'distance': 7.5,
                'fare': 40.00,
                'estimated_time': 30.0,
            },
            {
                'route_name': 'Banani to UAP Campus',
                'start_point': 'Banani 11',
                'end_point': 'UAP Campus, Green Road',
                'distance': 6.0,
                'fare': 35.00,
                'estimated_time': 25.0,
            },
            {
                'route_name': 'Motijheel to UAP Campus',
                'start_point': 'Motijheel CBD',
                'end_point': 'UAP Campus, Green Road',
                'distance': 8.0,
                'fare': 30.00,
                'estimated_time': 40.0,
            },
            {
                'route_name': 'Shyamoli to UAP Campus',
                'start_point': 'Shyamoli Square',
                'end_point': 'UAP Campus, Green Road',
                'distance': 4.5,
                'fare': 20.00,
                'estimated_time': 20.0,
            },
            {
                'route_name': 'Badda to UAP Campus',
                'start_point': 'Badda Link Road',
                'end_point': 'UAP Campus, Green Road',
                'distance': 9.0,
                'fare': 45.00,
                'estimated_time': 35.0,
            }
        ]
        
        # Create routes
        routes_created = 0
        for route_data in dhaka_routes:
            # Check if route already exists
            if not Route.objects.filter(route_name=route_data['route_name']).exists():
                route = Route.objects.create(
                    route_name=route_data['route_name'],
                    start_point=route_data['start_point'],
                    end_point=route_data['end_point'],
                    distance=route_data['distance'],
                    fare=route_data['fare'],
                    estimated_time=route_data['estimated_time'],
                    is_active=True
                )
                routes_created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created route: {route.route_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'↻ Route already exists: {route_data["route_name"]}'))
        
        # Get existing buses or create simple ones if none exist
        existing_buses = list(Bus.objects.all())
        
        if not existing_buses:
            self.stdout.write('No existing buses found. Creating basic buses...')
            basic_buses = [
                {'bus_number': 'UAP-101', 'capacity': 40, 'bus_name': 'Green Express'},
                {'bus_number': 'UAP-102', 'capacity': 35, 'bus_name': 'City Rider'},
                {'bus_number': 'UAP-201', 'capacity': 45, 'bus_name': 'Campus Cruiser'},
                {'bus_number': 'UAP-202', 'capacity': 38, 'bus_name': 'Road Master'},
            ]
            
            for bus_data in basic_buses:
                bus = Bus.objects.create(**bus_data)
                existing_buses.append(bus)
                self.stdout.write(self.style.SUCCESS(f'✓ Created bus: {bus.bus_number}'))
        else:
            self.stdout.write(f'Using {len(existing_buses)} existing buses')
        
        # Create schedules for each route
        schedule_count = 0
        routes = Route.objects.all()
        
        for route in routes:
            # Skip if route already has schedules
            if Schedule.objects.filter(route=route).exists():
                self.stdout.write(self.style.WARNING(f'↻ Skipping {route.route_name} - already has schedules'))
                continue
                
            # Morning schedules (for classes)
            morning_times = [
                (time(7, 0), (datetime.combine(date.today(), time(7, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(7, 30), (datetime.combine(date.today(), time(7, 30)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(8, 0), (datetime.combine(date.today(), time(8, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(8, 30), (datetime.combine(date.today(), time(8, 30)) + timedelta(minutes=int(route.estimated_time))).time()),
            ]
            
            # Afternoon schedules
            afternoon_times = [
                (time(14, 0), (datetime.combine(date.today(), time(14, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(14, 30), (datetime.combine(date.today(), time(14, 30)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(15, 0), (datetime.combine(date.today(), time(15, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
            ]
            
            # Evening schedules
            evening_times = [
                (time(17, 0), (datetime.combine(date.today(), time(17, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(17, 30), (datetime.combine(date.today(), time(17, 30)) + timedelta(minutes=int(route.estimated_time))).time()),
                (time(18, 0), (datetime.combine(date.today(), time(18, 0)) + timedelta(minutes=int(route.estimated_time))).time()),
            ]
            
            all_times = morning_times + afternoon_times + evening_times
            
            for i, (dep_time, arr_time) in enumerate(all_times):
                bus = existing_buses[i % len(existing_buses)]
                
                schedule = Schedule.objects.create(
                    bus=bus,
                    route=route,
                    departure_time=dep_time,
                    arrival_time=arr_time,
                    available_seats=bus.capacity
                )
                schedule_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'🎉 Successfully processed {routes_created} new routes and {schedule_count} schedules!'
        ))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('📍 Available Routes:'))
        for route in Route.objects.filter(is_active=True):
            self.stdout.write(f'   • {route.start_point} → {route.end_point} (৳{route.fare})')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🚌 Buses are now ready for booking!'))
