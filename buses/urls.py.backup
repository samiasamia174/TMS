from django.urls import path
from . import views
from .views_booking import booking_list, route_schedules, book_seat, my_bookings, cancel_booking

app_name = 'buses'

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    
    # Booking URLs
    path('booking/', booking_list, name='booking'),
    path('booking/route/<int:route_id>/', route_schedules, name='route_schedules'),
    path('booking/book/<int:schedule_id>/', book_seat, name='book_seat'),
    path('booking/my-bookings/', my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    
    # Route and Bus URLs
    path('', views.home, name='home'),
    path('routes/', views.route_list, name='route_list'),
    path('buses/', views.bus_list, name='bus_list'),
]
