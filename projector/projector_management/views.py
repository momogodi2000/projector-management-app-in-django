##@ author momo yvan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm
from django.urls import reverse
from .models import Projector, Booking, AdminNotification
from .forms import ProjectorForm,BookingForm, ValidateBookingForm
from django.contrib.auth import logout
from django.contrib import messages
from .models import Withdrawal, Deposit
from .decorators import admin_required




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




@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'dashboard/crud_user/manage_users.html', {'users': users})

@admin_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'dashboard/crud_user/add_user.html', {'form': form})

@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/crud_user/edit_user.html', {'form': form, 'user': user})

@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')
    return render(request, 'dashboard/crud_user/delete_user.html', {'user': user})

@admin_required
def manage_projectors(request):
    projectors = Projector.objects.all()
    return render(request, 'dashboard/crud_projector/manage_projectors.html', {'projectors': projectors})

@admin_required
def add_projector(request):
    if request.method == 'POST':
        form = ProjectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_projectors')
    else:
        form = ProjectorForm()
    return render(request, 'dashboard/crud_projector/add_projector.html', {'form': form})

@admin_required
def edit_projector(request, pk):
    projector = get_object_or_404(Projector, pk=pk)
    if request.method == 'POST':
        form = ProjectorForm(request.POST, request.FILES, instance=projector)
        if form.is_valid():
            form.save()
            return redirect('manage_projectors')
    else:
        form = ProjectorForm(instance=projector)
    return render(request, 'dashboard/crud_projector/edit_projector.html', {'form': form})

@admin_required
def delete_projector(request, pk):
    projector = get_object_or_404(Projector, pk=pk)
    if request.method == 'POST':
        projector.delete()
        return redirect('manage_projectors')
    return render(request, 'dashboard/crud_projector/delete_projector.html', {'projector': projector})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')





def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda user: user.is_superuser)(view_func))
    return decorated_view_func

@admin_required
def manage_withdrawals(request):
    withdrawals = Withdrawal.objects.all()
    return render(request, 'dashboard/status/manage_withdrawals.html', {'withdrawals': withdrawals})

@admin_required
def manage_deposits(request):
    deposits = Deposit.objects.all()
    return render(request, 'dashboard/status/manage_deposits.html', {'deposits': deposits})

def about_aics(request):
    return render(request, 'dashboard/status/about_aics.html')


@login_required
def book_projector(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 'Pending'
            booking.save()
            # Create notification for admin
            AdminNotification.objects.create(
                user=request.user,
                projector=booking.projector,
                booking=booking,
                notification_type='booking'
            )
            return redirect('user_dashboard')
    else:
        form = BookingForm()
    return render(request, 'request/book_projector.html', {'form': form})

@login_required
def validate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            booking.status = 'Approved'
        elif action == 'reject':
            booking.status = 'Rejected'
        booking.save()
        return redirect('admin_dashboard')
    return render(request, 'request/validate_booking.html', {'booking': booking})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    users = User.objects.all()
    notifications = AdminNotification.objects.filter(notification_type='booking', is_seen=False)
    context = {
        'notifications': notifications,
        'users': users
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


