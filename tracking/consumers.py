# tracking/consumers.py - পুরো file replace করুন

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Bus, BusLocation, Vehicle, BusStatus
from django.utils import timezone


class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authentication check
        if self.scope["user"] == AnonymousUser():
            await self.close(code=4001)
            return

        self.user = self.scope["user"]
        self.groups = ["tracking_all"]

        # Join tracking groups
        for group in self.groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            )

        await self.accept()

        # Send initial bus locations
        await self.send_initial_locations()

    async def disconnect(self, close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(
                group,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'subscribe_bus':
                bus_id = data.get('bus_id')
                if bus_id:
                    await self.subscribe_to_bus(bus_id)

            elif message_type == 'unsubscribe_bus':
                bus_id = data.get('bus_id')
                if bus_id:
                    await self.unsubscribe_from_bus(bus_id)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))

    async def subscribe_to_bus(self, bus_id):
        """Subscribe to specific bus updates"""
        group_name = f"bus_{bus_id}"
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        self.groups.append(group_name)

        # Send current bus location
        await self.send_bus_location(bus_id)

    async def unsubscribe_from_bus(self, bus_id):
        """Unsubscribe from specific bus updates"""
        group_name = f"bus_{bus_id}"
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )
        if group_name in self.groups:
            self.groups.remove(group_name)

    async def send_initial_locations(self):
        """Send initial locations of all active buses"""
        buses_data = await self.get_active_buses_locations()
        await self.send(text_data=json.dumps({
            'type': 'initial_locations',
            'data': buses_data
        }))

    async def send_bus_location(self, bus_id):
        """Send current location of specific bus"""
        bus_data = await self.get_bus_location(bus_id)
        if bus_data:
            await self.send(text_data=json.dumps({
                'type': 'bus_location',
                'data': bus_data
            }))

    @database_sync_to_async
    def get_active_buses_locations(self):
        """Get locations of all active buses"""
        buses = Bus.objects.filter(status='active')
        buses_data = []

        for bus in buses:
            try:
                location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
                buses_data.append({
                    'bus_id': bus.id,
                    'bus_number': bus.bus_number,
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude),
                    'speed': float(location.speed) if location.speed else 0,
                    'heading': float(location.heading) if location.heading else 0,
                    'timestamp': location.timestamp.isoformat(),
                    'status': await self.get_bus_status(bus.id)
                })
            except BusLocation.DoesNotExist:
                continue

        return buses_data

    @database_sync_to_async
    def get_bus_location(self, bus_id):
        """Get location of specific bus"""
        try:
            bus = Bus.objects.get(id=bus_id)
            location = BusLocation.objects.filter(bus=bus, is_active=True).latest()
            return {
                'bus_id': bus.id,
                'bus_number': bus.bus_number,
                'latitude': float(location.latitude),
                'longitude': float(location.longitude),
                'speed': float(location.speed) if location.speed else 0,
                'heading': float(location.heading) if location.heading else 0,
                'timestamp': location.timestamp.isoformat(),
                'status': await self.get_bus_status(bus.id)
            }
        except (Bus.DoesNotExist, BusLocation.DoesNotExist):
            return None

    @database_sync_to_async
    def get_bus_status(self, bus_id):
        """Get bus status"""
        try:
            status = BusStatus.objects.get(bus_id=bus_id)
            return {
                'status': status.status,
                'current_stop': status.current_stop,
                'delay_minutes': status.delay_minutes
            }
        except BusStatus.DoesNotExist:
            return {
                'status': 'not_running',
                'current_stop': '',
                'delay_minutes': 0
            }

    # Handle different types of updates
    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'data': event['data']
        }))

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': event['data']
        }))

    async def notification_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification_update',
            'data': event['data']
        }))