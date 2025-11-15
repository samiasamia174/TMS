from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Your existing signup view - enhanced with messages
from django.shortcuts import render

def signup(request):
    User = get_user_model()
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validation
        if not username:
            messages.error(request, 'Please enter a username.')
            return render(request, 'auth/signup.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another.')
            return render(request, 'auth/signup.html')
            
        if not password1 or not password2:
            messages.error(request, 'Please enter both password fields.')
            return render(request, 'auth/signup.html')
            
        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'auth/signup.html')
            
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'auth/signup.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password1
            )
            
            # Log the user in
            login(request, user)
            
            # Success message
            messages.success(request, f'🎉 Welcome to UAP Transportation, {username}! Your account has been created successfully.')
            
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'auth/signup.html')
    
    return render(request, 'auth/signup.html')

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Handle next parameter for redirect
            next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/signin.html', {'form': form, 'next': request.GET.get('next', '')})

def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Keep your existing views below this line
# ... your other view functions ...

# ===== BUS ROUTES VIEWS =====
from .models import Route, Bus, Schedule

def home(request):
    """Home page with route overview"""
    routes = Route.objects.filter(is_active=True).order_by('start_point')[:6]
    routes_count = Route.objects.filter(is_active=True).count()
    buses_count = Bus.objects.filter(is_active=True).count()
    
    context = {
        'routes': routes,
        'routes_count': routes_count,
        'buses_count': buses_count
    }
    return render(request, 'home.html', context)

def route_list(request):
    """Display all bus routes"""
    routes = Route.objects.filter(is_active=True).order_by('start_point')
    context = {
        'routes': routes
    }
    return render(request, 'routes/list.html', context)

def bus_list(request):
    """Display all buses"""
    buses = Bus.objects.filter(is_active=True).order_by('bus_number')
    context = {
        'buses': buses
    }
    return render(request, 'buses/list.html', context)

# ===== MAIN VIEWS =====
def home(request):
    """Home page with route overview"""
    routes = Route.objects.filter(is_active=True).order_by('start_point')[:6]
    routes_count = Route.objects.filter(is_active=True).count()
    buses_count = Bus.objects.filter(is_active=True).count()
    
    context = {
        'routes': routes,
        'routes_count': routes_count,
        'buses_count': buses_count
    }
    return render(request, 'home.html', context)

def route_list(request):
    """Display all bus routes"""
    routes = Route.objects.filter(is_active=True).order_by('start_point')
    context = {
        'routes': routes
    }
    return render(request, 'routes/list.html', context)

@login_required
def booking_view(request):
    """Booking page with routes and schedules"""
    routes = Route.objects.filter(is_active=True).order_by('start_point')
    schedules = Schedule.objects.filter(is_active=True).select_related('route', 'bus')
    
    context = {
        'routes': routes,
        'schedules': schedules
    }
    return render(request, 'booking/booking.html', context)

def dashboard(request):
    """User dashboard view"""
    return render(request, 'dashboard.html')

@login_required
@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'username': user.username,
        'email': user.email if user.email else 'Not set',
        'date_joined': user.date_joined,
    }
    return render(request, 'auth/profile.html', context)

# Authority Panel Views
@login_required
def authority_panel(request):
    return render(request, 'authority/panel.html')

@login_required
def manage_buses(request):
    return render(request, 'authority/manage_buses.html')

@login_required
def manage_routes(request):
    return render(request, 'authority/manage_routes.html')

@login_required
def manage_schedules(request):
    return render(request, 'authority/manage_schedules.html')

@login_required
def view_bookings(request):
    return render(request, 'authority/view_bookings.html')

# Bus Registration Flow Views
@login_required
def bus_registration(request):
    return render(request, 'registration/bus_registration.html')

@login_required
def search_routes(request):
    return render(request, 'registration/search_routes.html')

@login_required
def search_results(request):
    return render(request, 'registration/search_results.html')

@login_required
def select_bus(request):
    return render(request, 'registration/select_bus.html')

@login_required
def make_payment(request):
    return render(request, 'registration/make_payment.html')

@login_required
def confirmation(request):
    return render(request, 'registration/confirmation.html')

def contact_us(request):
    return render(request, 'contact.html')

def simple_profile(request):
    return render(request, 'profile.html')
