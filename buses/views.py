from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import Bus
from .forms import BusRegistrationForm, BusEditForm

# Home and Basic Views
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    total_buses = Bus.objects.count()
    active_buses = Bus.objects.filter(is_active=True).count()
    total_capacity = Bus.objects.aggregate(total=Sum('capacity'))['total'] or 0
    recent_buses = Bus.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_buses': total_buses,
        'active_buses': active_buses,
        'total_capacity': total_capacity,
        'recent_buses': recent_buses,
    }
    return render(request, 'dashboard.html', context)

def profile(request):
    return render(request, 'profile.html')

def contact_us(request):
    return render(request, 'contact_us.html')

# Authentication Views
def signup(request):
    User = get_user_model()
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        errors = []
        if not username:
            errors.append('Username is required.')
        if not password1:
            errors.append('Password is required.')
        elif len(password1) < 8:
            errors.append('Password must be at least 8 characters.')
        if password1 != password2:
            errors.append('Passwords do not match.')
        if username and User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not errors:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1
                )
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Authentication failed after account creation.')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for error in errors:
                messages.error(request, error)
    
    return render(request, 'registration/signup.html')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/signin.html', {'form': form})

def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Authority Panel Views
def authority_panel(request):
    return render(request, 'authority/panel.html')

def manage_routes(request):
    return render(request, 'authority/manage_routes.html')

def manage_schedules(request):
    return render(request, 'authority/manage_schedules.html')

def view_bookings(request):
    return render(request, 'authority/view_bookings.html')

# Bus Management Views
def bus_registration(request):
    if request.method == 'POST':
        form = BusRegistrationForm(request.POST)
        if form.is_valid():
            bus = form.save()
            messages.success(request, f'Bus {bus.bus_number} - {bus.bus_name} registered successfully!')
            return redirect('manage_buses')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusRegistrationForm()
    return render(request, 'buses/bus_registration.html', {'form': form, 'title': 'Register New Bus'})

def manage_buses(request):
    buses = Bus.objects.all().order_by('-created_at')
    return render(request, 'buses/manage_buses.html', {'buses': buses, 'title': 'Manage Buses'})

def edit_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        form = BusEditForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bus {bus.bus_number} updated successfully!')
            return redirect('manage_buses')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusEditForm(instance=bus)
    return render(request, 'buses/bus_registration.html', {'form': form, 'bus': bus, 'title': f'Edit Bus - {bus.bus_number}'})

def toggle_bus_status(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    bus.is_active = not bus.is_active
    bus.save()
    action = 'activated' if bus.is_active else 'deactivated'
    messages.success(request, f'Bus {bus.bus_number} {action} successfully!')
    return redirect('manage_buses')

def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    bus_number = bus.bus_number
    bus.delete()
    messages.success(request, f'Bus {bus_number} deleted successfully!')
    return redirect('manage_buses')

# Search and Booking Views
def search_routes(request):
    return render(request, 'buses/search_routes.html')

def search_results(request):
    return render(request, 'buses/search_results.html')

def select_bus(request):
    return render(request, 'buses/select_bus.html')

def make_payment(request):
    return render(request, 'buses/make_payment.html')

def confirmation(request):
    return render(request, 'buses/confirmation.html')
