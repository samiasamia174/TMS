from django.core.management.base import BaseCommand
from buses.models import Route
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add Dhaka city bus routes including UAP campus'

    def handle(self, *args, **options):
        # Dhaka city bus routes
        routes_data = [
            {
                'route_name': 'UAP Green Road to Farmgate',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Farmgate',
                'fare': 25.00,
                'distance': 5.0,
                'estimated_time': 20,
                'stops': 'Green Road, Pan Pacific, Sonargaon, Kawran Bazar, Farmgate',
                'is_active': True
            },
            {
                'route_name': 'UAP to Dhanmondi',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Dhanmondi 32',
                'fare': 30.00,
                'distance': 6.0,
                'estimated_time': 25,
                'stops': 'Green Road, New Market, Science Lab, Dhanmondi 27, Dhanmondi 32',
                'is_active': True
            },
            {
                'route_name': 'UAP to Gulshan 1',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Gulshan 1 Circle',
                'fare': 40.00,
                'distance': 8.0,
                'estimated_time': 35,
                'stops': 'Green Road, Moghbazar, Malibagh, Rampura, Badda, Gulshan 1',
                'is_active': True
            },
            {
                'route_name': 'UAP to Uttara',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Uttara Sector 7',
                'fare': 60.00,
                'distance': 18.0,
                'estimated_time': 60,
                'stops': 'Green Road, Shahbagh, Kakrail, Malibagh, Mohakhali, Airport, Uttara',
                'is_active': True
            },
            {
                'route_name': 'UAP to Mirpur 10',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Mirpur 10',
                'fare': 35.00,
                'distance': 10.0,
                'estimated_time': 40,
                'stops': 'Green Road, Shahbagh, Kakrail, Gabtoli, Mirpur 1, Mirpur 10',
                'is_active': True
            },
            {
                'route_name': 'UAP to Bashundhara',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Bashundhara Gate',
                'fare': 45.00,
                'distance': 12.0,
                'estimated_time': 45,
                'stops': 'Green Road, Moghbazar, Malibagh, Rampura, Kuril, Bashundhara',
                'is_active': True
            },
            {
                'route_name': 'UAP to Motijheel',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Motijheel',
                'fare': 20.00,
                'distance': 4.0,
                'estimated_time': 15,
                'stops': 'Green Road, Moghbazar, Fakirapool, Motijheel',
                'is_active': True
            },
            {
                'route_name': 'UAP to Mohammadpur',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Mohammadpur Town Hall',
                'fare': 30.00,
                'distance': 7.0,
                'estimated_time': 30,
                'stops': 'Green Road, New Market, Science Lab, Shankar, Mohammadpur',
                'is_active': True
            },
            {
                'route_name': 'UAP to Jatrabari',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Jatrabari',
                'fare': 35.00,
                'distance': 9.0,
                'estimated_time': 35,
                'stops': 'Green Road, Moghbazar, Fakirapool, Gulistan, Jatrabari',
                'is_active': True
            },
            {
                'route_name': 'UAP to Airport',
                'start_point': 'UAP Campus, Green Road',
                'end_point': 'Hazrat Shahjalal Airport',
                'fare': 50.00,
                'distance': 15.0,
                'estimated_time': 50,
                'stops': 'Green Road, Moghbazar, Malibagh, Rampura, Badda, Kuril, Airport',
                'is_active': True
            }
        ]

        # Create routes
        for route_data in routes_data:
            route, created = Route.objects.get_or_create(
                route_name=route_data['route_name'],
                defaults=route_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created route: {route.route_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Route already exists: {route.route_name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully added all Dhaka city bus routes!')
        )
