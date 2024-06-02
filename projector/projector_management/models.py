##@ author momo yvan
from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Projector(models.Model):
    name = models.CharField(max_length=100, default='Default Projector Name')
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    quantity_min = models.IntegerField(default=1)
    quantity_max = models.IntegerField(default=10)
    model_type = models.CharField(max_length=255, default='HP')  # Ensure this line is present
    serial_number = models.CharField(max_length=255, unique=True, default='02013948439992')
    image = models.ImageField(upload_to='projectors_images/', null=True, blank=True)

    @property
    def status(self):
        if self.quantity <= self.quantity_min:
            return "Stock Alert"
        elif self.quantity >= self.quantity_max:
            return "Full Stock"
        else:
            return "In Stock"

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    devices = models.ManyToManyField(Device, blank=True)

class Deposit(models.Model):
    withdrawal = models.ForeignKey(Withdrawal, on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now_add=True)
    returned_devices = models.ManyToManyField(Device, blank=True)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    is_booked = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE)
    booking_date = models.DateField() 
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.projector.name}"

class AdminNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=255, choices=[('booking', 'Booking'), ('approval', 'Approval'), ('rejection', 'Rejection')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()} - {self.projector.model_type}"

