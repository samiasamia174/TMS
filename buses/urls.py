from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
]

# Booking URLs
from .views_booking import booking_list, route_schedules, book_seat, my_bookings, cancel_booking

urlpatterns += [
    path('booking/', booking_list, name='booking'),
    path('booking/route/<int:route_id>/', route_schedules, name='route_schedules'),
    path('booking/book/<int:schedule_id>/', book_seat, name='book_seat'),
    path('booking/my-bookings/', my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]

# Route and Bus URLs
from .views import home, route_list, bus_list

urlpatterns += [
    path('', home, name='home'),
    path('routes/', route_list, name='route_list'),
    path('buses/', bus_list, name='bus_list'),
]
