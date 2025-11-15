# Read the current views.py
with open('buses/views.py', 'r') as f:
    content = f.read()

# Check if we need to update the signin function
if "request.POST.get('next')" not in content:
    print("Updating signin view...")
    
    # Create the updated signin function
    new_signin = '''def signin(request):
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
    
    return render(request, 'auth/signin.html', {'form': form, 'next': request.GET.get('next', '')})'''

    # Replace the signin function using a more robust method
    import re
    # Find the signin function and replace it
    pattern = r'def signin\(request\):.*?return render\(request, [\'"]auth/signin\.html[\'"], {\'form\': form}\)'
    content = re.sub(pattern, new_signin, content, flags=re.DOTALL)
    
    # Write back
    with open('buses/views.py', 'w') as f:
        f.write(content)
    print("Signin view updated successfully!")
else:
    print("Signin view already has next parameter handling")
