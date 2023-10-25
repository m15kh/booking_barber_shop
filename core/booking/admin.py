from django.contrib import admin
from .models import Barber, Appointment, Appointment_Hour
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Barber)
admin.site.register(Appointment_Hour)