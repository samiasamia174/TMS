from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from buses.models import UserProfile, Schedule
from datetime import date

User = get_user_model()

def home(request):
    """Home page"""
    return render(request, 'home.html')

def bus_schedule(request):
    """Bus schedule page"""
    schedules = Schedule.objects.all() if hasattr(Schedule, 'objects') else []
    return render(request, 'buses/schedule.html', {'schedules': schedules})

def search_results(request):
    """Search results page"""
    return render(request, 'bus/search_results.html')

def bus_registration(request):
    """Bus registration page"""
    return render(request, 'buses/bus_registration.html')

def confirmation(request):
    """Confirmation page"""
    return render(request, 'buses/confirmation.html')

def contact_us(request):
    """Contact us page"""
    return render(request, 'buses/contact_us.html')

def search_routes(request):
    """Search routes page"""
    return render(request, 'buses/search_routes.html')

def select_bus(request):
    """Select bus page"""
    return render(request, 'buses/select_bus.html')

def make_payment(request):
    """Make payment page"""
    return render(request, 'buses/make_payment.html')

def signup(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type', 'student')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        student_id = request.POST.get('student_id', '')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'auth/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'auth/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'auth/signup.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                student_id=student_id,
                phone=phone,
                address=address
            )

            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('signin')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')

def signin(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'auth/signin.html')

def sign_out(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been successfully signed out!')
    return redirect('dashboard')

def dashboard(request):
    """User dashboard"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/dashboard.html', {'user': request.user})

def profile(request):
    """User profile"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/profile.html', {'user': request.user})

def authority_panel(request):
    """Authority panel"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/authority_panel.html', {'user': request.user})

def manage_buses(request):
    """Manage buses"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/manage_buses.html', {'user': request.user})

def manage_routes(request):
    """Manage routes"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/manage_routes.html', {'user': request.user})

def manage_schedules(request):
    """Manage schedules"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/manage_schedules.html', {'user': request.user})

def view_bookings(request):
    """View bookings"""
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'buses/view_bookings.html', {'user': request.user})
