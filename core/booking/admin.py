from django.contrib import admin
from .models import Barber, TimeRange, Booking
# Register your models here.

class TimeRangeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'workstart', 'workfinish', 'reststart', 'restfinish', 'duration')
    
    # Define a custom ordering based on the name of the day
    ordering = ('Days',)

admin.site.register(TimeRange, TimeRangeAdmin)

admin.site.register(Barber)
admin.site.register(Booking)
