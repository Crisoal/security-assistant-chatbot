# users/views.py
import logging
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from chatbot.models import UserProgress
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from .models import CustomUser

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically add user to 'User' group
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# users/views.py
@login_required
def dashboard_view(request):
    user = request.user

    # If role is not set, redirect to role selection page
    if user.role is None:
        return redirect('role_selection')

    return render(request, 'dashboard.html', {'user': user})

@login_required
def role_selection(request):
    if request.method == "POST":
        selected_role = request.POST.get("role")
        logger.info(f"Received role: {selected_role}")  # Debugging

        if selected_role in dict(CustomUser.ROLE_CHOICES).keys():
            request.user.role = selected_role
            request.user.save()
            return JsonResponse({"success": True})

        logger.error("Invalid role selection")  # Log the issue
        return JsonResponse({"error": "Invalid role selection"}, status=400)

    return render(request, 'role_selection.html')

def csrf_failure(request, reason=""):
    
    return JsonResponse({
        'error': 'CSRF token missing or invalid',
        'status': 403
    }, status=403)