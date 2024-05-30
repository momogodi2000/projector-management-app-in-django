from django import forms
from django.contrib.auth.models import User
from .models import Projector

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
        fields = ['model_type', 'park_type', 'serial_number', 'image']