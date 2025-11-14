from django.urls import path
from . import views

app_name = 'buses'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule/', views.bus_schedule, name='bus_schedule'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
    path('authority-panel/', views.authority_panel, name='authority_panel'),
    path('authority/buses/', views.manage_buses, name='manage_buses'),
    path('authority/routes/', views.manage_routes, name='manage_routes'),
    path('authority/schedules/', views.manage_schedules, name='manage_schedules'),
    path('authority/bookings/', views.view_bookings, name='view_bookings'),
    path('bus-registration/', views.bus_registration, name='bus_registration'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('search-results/', views.search_results, name='search_results'),
    path('select-bus/', views.select_bus, name='select_bus'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('contact-us/', views.contact_us, name='contact_us'),
]