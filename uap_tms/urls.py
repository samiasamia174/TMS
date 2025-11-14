from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView
from buses import views

urlpatterns = [
    path("schedule/", lambda request: redirect("search_routes")),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Fix for broken signup links
    path('"/signup//"', RedirectView.as_view(url='/signup/', permanent=False)),
    path('%22/signup//%22', RedirectView.as_view(url='/signup/', permanent=False)),
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
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
