from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

def enhanced_signup(request):
    """Enhanced signup view with better user feedback"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Basic validation
        if not username:
            messages.error(request, 'Please enter a username.')
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
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another.')
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
            messages.success(request, f'Welcome to UAP Transportation, {username}! Your account has been created successfully.')
            
            # Redirect to dashboard
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'auth/signup.html')
    
    # GET request - show empty form
    return render(request, 'auth/signup.html')

def enhanced_signin(request):
    """Enhanced signin view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/signin.html', {'form': form})
