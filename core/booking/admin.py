from django.contrib import admin
from .models import TimeRange, Booking, ExcludedDates
from django.core.exceptions import ValidationError

# Register your models here.
from django.contrib import messages


class TimeRangeAdmin(admin.ModelAdmin):
    
    
    
    
    list_filter = ()

    def get_list_filter(self, request):
        # Check if the user is an admin
        if request.user.role == "ADMIN":
            # Show "barber" and "Days" in list filter for admins
            return super().get_list_filter(request) + ("barber", "Days")
        return super().get_list_filter(request) + ("Days",)

    list_display = (
        "barber_id",
        "barber",
        "__str__",
        "formatted_workstart",
        "formatted_workfinish",
        "formatted_reststart",
        "formatted_restfinish",
        "duration",
    )
    list_display_links = (
        "barber_id",
        "barber",
    )

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


@admin.register(TimeRange)

class CustomTimeRangeAdmin(TimeRangeAdmin):

    exclude = ()

    def get_form(self, request, obj=None, **kwargs):
        # Check if the user is an admin
        if hasattr(request.user, "barberprofile"):
            self.exclude = ("barber", "number_timeslots")

        else:
            self.exclude = ("number_timeslots",)

        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "ADMIN":
            return qs.all()
        elif request.user.role == "BARBERUSER":
            return qs.filter(barber=request.user.barberprofile)
        else:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if request.user.role == "ADMIN":
            obj.barber  = obj.barber
        elif request.user.role == "BARBERUSER":
            # Set the barber field to the logged-in user's BarberProfile
            obj.barber = request.user.barberprofile

            # Check if the barber already has an active time range for the same day
            existing_time_range = (
                TimeRange.objects.filter(
                    barber=request.user.barberprofile,
                    Days=obj.Days,
                )
                .exclude(pk=obj.pk if obj.pk else None)
                .first()
            )
            if existing_time_range:
                messages.set_level(request, messages.ERROR)
                message = f"A time range already exists for {request.user.barberprofile} on {obj.Days}."
                self.message_user(request, message, level=messages.ERROR)
                return

        super().save_model(request, obj, form, change)

