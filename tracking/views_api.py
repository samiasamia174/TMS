from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer
from transport.models import Bus

class BusLocationDetail(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        bus_id = self.kwargs['bus_id']
        return Location.objects.get(bus_id=bus_id)

class BusLocationUpdate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        bus_id = request.data.get('bus_id')
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        if not all([bus_id, lat, lng]):
            return Response({"detail":"bus_id, lat, lng required"}, status=400)
        bus = Bus.objects.get(id=bus_id)
        location, _ = Location.objects.get_or_create(bus=bus, defaults={'lat': lat, 'lng': lng})
        location.lat = lat
        location.lng = lng
        location.save()
        return Response(LocationSerializer(location).data)
