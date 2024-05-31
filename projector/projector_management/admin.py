from django.contrib import admin

from django.contrib import admin
from .models import Device, Projector, Withdrawal, Deposit, Booking, AdminNotification

admin.site.register(Device)
admin.site.register(Projector)
admin.site.register(Withdrawal)
admin.site.register(Deposit)
admin.site.register(Booking)
admin.site.register(AdminNotification)
