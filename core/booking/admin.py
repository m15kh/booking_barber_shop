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


admin.site.register(TimeRange, TimeRangeAdmin)


admin.site.register(Booking)
