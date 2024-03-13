from django.contrib import admin
from .models import TimeRange, Booking, ExcludedDates
from django.urls import reverse

from django.urls import reverse
from django.utils.html import format_html

from datetime import timedelta, datetime


# Register your models here.
from django.contrib import messages


class TimeRangeAdmin(admin.ModelAdmin):

    list_filter = ()

    def get_list_filter(self, request):
        if request.user.role == "ADMIN":
            # Show "barber" and "Days" in list filter for admins
            return super().get_list_filter(request) + ("barber", "Days")
        return super().get_list_filter(request) + ("Days",)

    list_display = (
        
        "barber",
        "__str__",
        "formatted_workstart",
        "formatted_workfinish",
        "formatted_reststart",
        "formatted_restfinish",
        "duration",
    )

    ordering = (
        "barber",
        "Days",
    )

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
        if request.user.role == "BARBERUSER":
            self.exclude = (
                "barber",
                "number_timeslots",
            )
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
            obj.barber = obj.barber
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




@admin.register(ExcludedDates)
class ExcludedDatesAdmin(admin.ModelAdmin):

    exclude = ()

    def get_form(self, request, obj=None, **kwargs):
        # Check if the user is an admin
        if request.user.role == "BARBERUSER":
            self.exclude = ("barber",)
        else:
            self.exclude = ()
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
            obj.barber = obj.barber
        elif request.user.role == "BARBERUSER":
            # Set the barber field to the logged-in user's BarberProfile
            obj.barber = request.user.barberprofile

            excluded_dated = (
                ExcludedDates.objects.filter(
                    barber=request.user.barberprofile,
                    date=obj.date,
                )
                .exclude(pk=obj.pk if obj.pk else None)
                .first()
            )
            if excluded_dated:
                messages.set_level(request, messages.ERROR)
                message = f"A time range already exists for {request.user.barberprofile} on {obj.date}."
                self.message_user(request, message, level=messages.ERROR)
                return

            super().save_model(request, obj, form, change)

    list_display = (
        "barber",
        "formatted_date",
    )
    "barber",

    def formatted_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    ordering = ("date",)


class DateFilter(admin.SimpleListFilter):
    title = "Date"
    parameter_name = "date"

    def lookups(self, request, model_admin):
        return (
            ("past", "Past Dates"),
            ("today", "Today"),
            ("tomorrow", "Tomorrow"),
            ("next_3_days", "Next 3 Days"),
            ("ongoing", "Ongoing Dates"),
        )

    def queryset(self, request, queryset):

        if self.value() == "past":
            today = datetime.now().date()
            current_time = datetime.now().time()
            return queryset.filter(date__lt=today) | queryset.filter(
                date=today, time__lt=current_time
            )

        elif self.value() == "today":
            today = datetime.now().date()
            current_time = datetime.now().time()
            return queryset.filter(date=today, time__gt=current_time)

        elif self.value() == "tomorrow":
            tomorrow = datetime.now().date() + timedelta(days=1)
            return queryset.filter(date=tomorrow)
        elif self.value() == "next_3_days":
            end_date = datetime.now().date() + timedelta(days=3)
            return queryset.filter(date__gte=datetime.now().date(), date__lte=end_date)
        elif self.value() == "ongoing":
            return queryset.filter(date__gte=datetime.now().date())

        else:
            return queryset


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "BARBERUSER":
            return qs.filter(barber=request.user.barberprofile)
        elif request.user.role == "ADMIN":
            return qs.all()
        else:
            return qs.none()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    ordering = (
        "date",
        "time",
    )

    list_display = (
        "barber",
        "formatted_date",
        "time_24",
        "name_week",
        "customer_link",
        "status",
    )

    list_filter = (
        DateFilter,
        "status",
        "barber",
    )

    def get_list_filter(self, request):
        if request.user.role == "ADMIN":
            return super().get_list_filter(request)
        else:
            return (DateFilter, "status")  # Default filter options if not admin

    list_per_page = 20

    def time_24(self, obj):
        return obj.time.strftime("%H:%M")

    def name_week(self, obj):
        return obj.date.strftime("%A")

    def formatted_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    list_display_links = (
        "time_24",
        'formatted_date'
    )

    def customer_link(self, obj):
        url = reverse(
            "admin:accounts_customeruser_change", args=[obj.customer.user.pk]
        )

        return format_html('<a href="{}">{}</a>', url, obj.customer)

    customer_link.short_description = "Customer Profile"

    search_fields = (
        "date",
         #edit by  search with phone nmuber
    )
