from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # Import login directly
from users.forms import CustomUserCreationForm
from django.contrib import messages # Import for displaying error messages

# ----------------------------------------------------------------------

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # NOTE: authenticate is called with the request object in modern Django
        user = authenticate(request, username=username, password=password) 

        if user is not None:
            # Successfully authenticated, log the user in
            login(request, user)
            return redirect('profile')  # Redirect after successful login
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password.')
            # Use redirect to clear the POST data, or render to show the message on the form
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    # For GET request, just render the empty form
    return render(request, 'login.html')

# ----------------------------------------------------------------------

def register_view(request):
    if request.method == "POST":
        # Pass request.FILES only if your form actually handles file uploads (e.g., a profile picture)
        form = CustomUserCreationForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            
            # CRITICAL MISTAKE CORRECTION: 
            # You were setting a variable named 'login' instead of calling the login function.
            login(request, user) 
            
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('profile') # Redirect after successful registration
        
        # If the form is not valid, it falls through and renders the form with errors
    else:
        # For GET request, create a blank form
        form = CustomUserCreationForm()
        
    # Render the registration template, passing the form (either blank or with errors)
    return render(request, "register.html", {'form': form})

# ----------------------------------------------------------------------

def log_out(request):
    # Log the user out
    logout(request)
    # Redirect to the login page (or whichever page you prefer after logout)
    return redirect('user_login')