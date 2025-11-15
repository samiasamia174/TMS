# tracking/views.py - এই class টি যোগ করুন

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Vehicle, Bus, BusLocation, BusStatus
from django.utils import timezone
import json


@method_decorator(csrf_exempt, name='dispatch')
class UpdateLocationView(View):
    def post(self, request):
        try:
            # Support both form data and JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            vehicle_id = data.get('vehicle_id')
            lat = float(data.get('latitude', 0))
            lng = float(data.get('longitude', 0))
            speed = data.get('speed')
            heading = data.get('heading')

            # Validate data
            if not vehicle_id:
                return JsonResponse({"status": "error", "message": "Vehicle ID required"})

            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return JsonResponse({"status": "error", "message": "Invalid coordinates"})

            # Update Vehicle
            vehicle, created = Vehicle.objects.update_or_create(
                vehicle_id=vehicle_id,
                defaults={
                    'latitude': lat,
                    'longitude': lng,
                    'name': vehicle_id
                }
            )

            # Update BusLocation if bus exists
            bus_data = self.update_bus_location(vehicle_id, lat, lng, speed, heading)

            # Broadcast to WebSocket groups
            self.broadcast_location_update(vehicle_id, bus_data, lat, lng, speed, heading)

            return JsonResponse({
                "status": "success",
                "bus_data": bus_data
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    def update_bus_location(self, vehicle_id, lat, lng, speed=None, heading=None):
        """Update BusLocation for corresponding bus"""
        try:
            bus = Bus.objects.get(bus_number=vehicle_id)

            # Deactivate previous locations
            BusLocation.objects.filter(bus=bus).update(is_active=False)

            # Create new location
            BusLocation.objects.create(
                bus=bus,
                latitude=lat,
                longitude=lng,
                speed=speed,
                heading=heading,
                is_active=True,
                timestamp=timezone.now()
            )

            # Update bus status last_updated
            try:
                bus_status = BusStatus.objects.get(bus=bus)
                bus_status.last_updated = timezone.now()
                bus_status.save()
            except BusStatus.DoesNotExist:
                pass

            return {
                'bus_id': bus.id,
                'bus_number': bus.bus_number,
                'exists': True
            }

        except Bus.DoesNotExist:
            return {
                'bus_id': None,
                'bus_number': vehicle_id,
                'exists': False
            }

    def broadcast_location_update(self, vehicle_id, bus_data, lat, lng, speed, heading):
        """Broadcast location update to WebSocket groups"""
        channel_layer = get_channel_layer()

        update_data = {
            "vehicle_id": vehicle_id,
            "bus_id": bus_data.get('bus_id'),
            "bus_number": bus_data.get('bus_number'),
            "latitude": lat,
            "longitude": lng,
            "speed": speed,
            "heading": heading,
            "timestamp": timezone.now().isoformat()
        }

        # Broadcast to all tracking group
        async_to_sync(channel_layer.group_send)(
            "tracking_all",
            {
                "type": "location_update",
                "data": update_data
            }
        )

        # Broadcast to specific bus group if exists
        if bus_data.get('bus_id'):
            async_to_sync(channel_layer.group_send)(
                f"bus_{bus_data['bus_id']}",
                {
                    "type": "location_update",
                    "data": update_data
                }
            )

    # tracking/views.py - live_tracking function update করুন

    @login_required
    def live_tracking(request):
        """Display live tracking map with WebSocket support"""
        buses = Bus.objects.filter(status='active')

        # Get latest location for each bus
        bus_locations = []
        for bus in buses:
            try:
                location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
                bus_status = getattr(bus, 'current_status', None)

                bus_locations.append({
                    'bus': bus,
                    'location': location,
                    'status': bus_status,
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude),
                    'speed': float(location.speed) if location.speed else 0,
                })
            except BusLocation.DoesNotExist:
                continue

        context = {
            'bus_locations': bus_locations,
            'websocket_url': 'ws://' + request.get_host() + '/ws/tracking/'
        }
        return render(request, 'tracking/live_tracking.html', context)