from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import RouteViewSet, BusViewSet, RegistrationViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'buses', BusViewSet)
router.register(r'registrations', RegistrationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
