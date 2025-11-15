from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from buses import views
from buses.views_booking import booking_list, route_schedules, book_seat, my_bookings, cancel_booking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Include apps
    path('buses/', include('buses.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile redirect - THIS IS THE KEY LINE
    path('profile/', RedirectView.as_view(url='/accounts/profile/', permanent=False), name='profile'),
    
    # Direct URLs for routes and booking
    path('routes/', views.route_list, name='routes'),
    path('booking/', booking_list, name='booking'),
    path('booking/route/<int:route_id>/', route_schedules, name='route_schedules'),
    path('booking/book/<int:schedule_id>/', book_seat, name='book_seat'),
    path('booking/my-bookings/', my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    
    # Authority Panel URLs
    path('authority-panel/', views.authority_panel, name='authority_panel'),
    path('authority/buses/', views.manage_buses, name='manage_buses'),
    path('authority/routes/', views.manage_routes, name='manage_routes'),
    path('authority/schedules/', views.manage_schedules, name='manage_schedules'),
    path('authority/bookings/', views.view_bookings, name='view_bookings'),
    
    # Bus Registration URLs
    path('bus-registration/', views.bus_registration, name='bus_registration'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('search-results/', views.search_results, name='search_results'),
    path('select-bus/', views.select_bus, name='select_bus'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
