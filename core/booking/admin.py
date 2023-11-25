from django.contrib import admin
from .models import TimeRange, Booking

# Register your models here.


class TimeRangeAdmin(admin.ModelAdmin):
    list_display = (
        "barber_id",
        "barber",
        "__str__",
        "workstart",
        "workfinish",
        "reststart",
        "restfinish",
        "duration",
    )
    list_display_links = (
        "barber_id",
        "barber",
    )

    # Define a custom ordering based on the name of the day
    list_filter = ("barber", "Days")
    ordering = ("barber", "Days")

class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "barber",
        "date",
        "formatted_timeslot",  # Use the custom method here
    )

    list_filter = ("barber", "date")
    ordering = ("barber", "date")

    def formatted_timeslot(self, obj):
        return obj.timeslot.strftime("%H:%M")

    formatted_timeslot.short_description = "Timeslot"  # Set a custom column header


admin.site.register(TimeRange, TimeRangeAdmin)


admin.site.register(Booking, BookingAdmin)
