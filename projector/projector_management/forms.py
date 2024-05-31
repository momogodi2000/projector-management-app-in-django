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

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'projector', 'booking_date']  # Exclude start_time and end_time fields

    start_time = forms.DateTimeField(label='Start Time', required=False)
    end_time = forms.DateTimeField(label='End Time', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:  # If editing an existing instance, populate start_time and end_time
            self.fields['start_time'].initial = instance.start_time
            self.fields['end_time'].initial = instance.end_time

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_time = self.cleaned_data.get('start_time')
        instance.end_time = self.cleaned_data.get('end_time')
        if commit:
            instance.save()
        return instance

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

