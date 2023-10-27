from django.contrib import admin
from .models import Barber, TimeRange, Booking
# Register your models here.
admin.site.register(TimeRange)
admin.site.register(Barber)
admin.site.register(Booking)