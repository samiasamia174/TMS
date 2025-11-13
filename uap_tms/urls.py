from django.contrib import admin
from django.urls import path, include
from buses import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('payment/', include('payments.urls')),
    # Authentication URLs - Added by Samia
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('', include('buses.urls')),  # register buses URL patterns so reverse('bus_schedule') resolves

    # Authority Panel URLs - Added by Samia
    path('authority-panel/', views.authority_panel, name='authority_panel'),
    path('authority/buses/', views.manage_buses, name='manage_buses'),
    path('authority/routes/', views.manage_routes, name='manage_routes'),
    path('authority/schedules/', views.manage_schedules, name='manage_schedules'),
    path('authority/bookings/', views.view_bookings, name='view_bookings'),
    
    # Bus Registration URLs - Added by Zakir
    path('bus-registration/', views.bus_registration, name='bus_registration'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('search-results/', views.search_results, name='search_results'),
    path('select-bus/', views.select_bus, name='select_bus'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('contact-us/', views.contact_us, name='contact_us'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

