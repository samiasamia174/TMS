from rest_framework import viewsets, permissions
from .models import Route, Bus, Registration
from .serializers import RouteSerializer, BusSerializer, RegistrationSerializer

class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.select_related('route').all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related('user','bus').all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if 'user' not in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
