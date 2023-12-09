from django.contrib import admin
from .models import TimeRange, Booking

# Register your models here.


class TimeRangeAdmin(admin.ModelAdmin):
    list_display = (
        "barber_id",
        "barber",
        "__str__",
        "formatted_workstart",
        "formatted_workfinish",  # Custom display for workfinish
        "formatted_reststart",  # Custom display for reststart
        "formatted_restfinish",  # Custom display for restfinish
        "duration",
    )
    list_display_links = (
        "barber_id",
        "barber",
    )

    # Define a custom ordering based on the name of the day
    list_filter = ("barber", "Days")
    ordering = ("barber", "Days")

    def formatted_workstart(self, obj):
        return obj.workstart.strftime("%H:%M")

    def formatted_workfinish(self, obj):
        return obj.workfinish.strftime("%H:%M")

    def formatted_reststart(self, obj):
        return obj.reststart.strftime("%H:%M")

    def formatted_restfinish(self, obj):
        return obj.restfinish.strftime("%H:%M")

    formatted_workstart.short_description = "workstart"
    formatted_workfinish.short_description = "workfinish"
    formatted_reststart.short_description = "reststart"
    formatted_restfinish.short_description = "restfinish"


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "barber",
        "date",
        "formatted_time",  # Use the custom method here
    )

    list_filter = ("barber", "date")
    ordering = ("barber", "date")

    raw_id_fields = ["customer"]

    def formatted_time(self, obj):
        return obj.time.strftime("%H:%M")

    formatted_time.short_description = "time"


admin.site.register(TimeRange, TimeRangeAdmin)


admin.site.register(Booking, BookingAdmin)
