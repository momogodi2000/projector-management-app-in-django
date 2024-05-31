##@ author momo yvan
from django import forms
from django.contrib.auth.models import User
from .models import Projector, Booking

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
class ProjectorForm(forms.ModelForm):
    class Meta:
        model = Projector
        fields = ['name', 'description', 'quantity', 'quantity_min', 'quantity_max', 'model_type', 'serial_number','image']



class ValidateBookingForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Booking
        fields = ['status']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['projector', 'booking_date', 'start_time', 'end_time']