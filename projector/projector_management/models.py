from django.db import models
from django.contrib.auth.models import User

class Projector(models.Model):
    model_type = models.CharField(max_length=255)
    park_type = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)  # Track specific projectors

class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Optional description

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    devices = models.ManyToManyField(Device, blank=True)  # Allow withdrawals without devices

class Deposit(models.Model):
    withdrawal = models.ForeignKey(Withdrawal, on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now_add=True)
    returned_devices = models.ManyToManyField(Device, blank=True)  # Track returned devices

class AdminNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the booking
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE)
    withdrawal = models.ForeignKey(Withdrawal, on_delete=models.CASCADE, null=True, blank=True)  # Optional FK for Withdrawal
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, null=True, blank=True)  # Optional FK for Deposit
    notification_type = models.CharField(max_length=255, choices=[('booking', 'Booking'), ('return', 'Return')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)  # Track if the admin has seen the notification

    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()} - {self.projector.model_type}"

