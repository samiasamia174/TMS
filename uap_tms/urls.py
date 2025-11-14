from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Simple views for main pages
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    return render(request, 'profile.html')

def buses_list(request):
    return render(request, 'buses/list.html')

def routes_list(request):
    return render(request, 'routes/list.html')

def booking_list(request):
    return render(request, 'booking/list.html')

def payment_list(request):
    return render(request, 'payment/list.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main pages - direct views
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('buses/', buses_list, name='buses'),
    path('routes/', routes_list, name='routes'),
    path('booking/', booking_list, name='booking'),
    path('payment/', payment_list, name='payment'),
    
    # Auth pages - include from buses app
    path('', include('buses.urls')),
]
