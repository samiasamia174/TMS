from django.contrib import admin
from django.urls import path, include
from buses import views
from buses.views_booking import booking_list, route_schedules, book_seat, my_bookings, cancel_booking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Include buses app
    path('buses/', include('buses.urls')),
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile - use our simple profile
    path('profile/', views.simple_profile, name='profile'),
    
    # Direct URLs for routes and booking
    path('routes/', views.route_list, name='routes'),
    path('booking/', booking_list, name='booking'),
    path('booking/route/<int:route_id>/', route_schedules, name='route_schedules'),
    path('booking/book/<int:schedule_id>/', book_seat, name='book_seat'),
    path('booking/my-bookings/', my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    
    # Contact us page
    path('contact-us/', views.contact_us, name='contact_us'),
]
