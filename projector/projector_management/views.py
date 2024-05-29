from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.urls import reverse

def home(request):
    context = {} 
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'auth/register.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # Implement password reset logic here
        messages.success(request, 'Password reset link sent to your email')
        return redirect('login')
    return render(request, 'auth/forgot_password.html')

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'dashboard/user_dashboard.html', {'user': request.user})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    users = User.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully')
            return redirect('admin_dashboard')
    else:
        form = UserForm()
    return render(request, 'dashboard/crud/add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('admin_dashboard')
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/crud/edit_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('admin_dashboard')
    return render(request, 'dashboard/crud/delete_user.html', {'user': user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    users = User.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'users': users})