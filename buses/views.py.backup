from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')

        # Create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Auto-login after signup
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')

    return render(request, 'signup.html')


def dashboard(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access dashboard')
        return redirect('signin')

    return render(request, 'dashboard.html')


def home(request):
    return render(request, 'home.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')