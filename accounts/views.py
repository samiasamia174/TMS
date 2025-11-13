from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
from .models import Profile


def home(request):
    """Home page view"""
    return render(request, 'accounts/home.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create empty profile
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:home')


@login_required
def dashboard(request):
    """User dashboard view"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    context = {
        'user': request.user,
        'profile': profile,
    }

    # Redirect to profile completion if not complete
    if not profile.is_profile_complete:
        messages.warning(request, 'Please complete your profile to continue.')
        return redirect('accounts:complete_profile')

    return render(request, 'accounts/dashboard.html', context)


@login_required
def complete_profile(request):
    """Complete user profile view"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_profile_complete = True
            profile.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/complete_profile.html', {'form': form})


@login_required
def profile(request):
    """View and edit user profile"""
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': user_profile})


@login_required
def control_panel(request):
    """Control panel for authority users"""
    if request.user.user_type != 'authority':
        messages.error(request, 'Access denied. Authority access required.')
        return redirect('accounts:dashboard')

    return render(request, 'accounts/control_panel.html')