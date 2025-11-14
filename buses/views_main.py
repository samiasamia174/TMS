from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
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
