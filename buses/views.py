@login_required
def dashboard(request):
    # User dashboard after login
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, user_type='student')

    context = {
        'user_profile': user_profile
    }
    return render(request, 'buses/dashboard.html', context)

def signup(request):
    # User registration/signup view
    if request.method == 'POST':
        # ... keep the full signup logic
        pass
    return render(request, 'auth/signup.html')

def signin(request):
    # User login/signin view
    if request.method == 'POST':
        # ... keep the full signin logic
        pass
    return render(request, 'auth/signin.html')

def sign_out(request):
    # User logout view
    logout(request)
    messages.success(request, 'You have been successfully signed out!')
    return redirect('home')

def make_payment(request):
    return render(request, 'bus/payment.html')