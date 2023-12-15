from django.views import View
from django.shortcuts import render
from accounts.models import BarberProfile
from booking.models import Booking, TimeRange
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

from django.http import HttpResponseForbidden


@method_decorator(login_required, name="dispatch")
class BarberPanelView(View):
    def get(self, request, barber_id):
        # Ensure that the user has a related BarberProfile
        if not hasattr(request.user, "barberprofile"):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        # Check if the requested barber_id matches the user's BarberProfile
        if request.user.barberprofile.id != int(barber_id):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        barber = BarberProfile.objects.get(pk=barber_id)
        tomorrow_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        upcoming_bookings = Booking.objects.filter(
            barber=barber,
            date__gte=tomorrow_date,
        ).order_by("date", "time")
        count_tomorrow_bookings = upcoming_bookings.count()

        today_bookings = Booking.objects.filter(
            barber=barber,
            date=datetime.today().strftime("%Y-%m-%d"),
            time__gt=datetime.now(),
        ).order_by("time")

        count_today_bookings = today_bookings.count()

        context = {
            "barber": barber,
            "upcoming_bookings": upcoming_bookings,
            "today_bookings": today_bookings,
            "count_today_bookings": count_today_bookings,
            "count_tomorrow_bookings": count_tomorrow_bookings,
        }
        return render(request, "barbers/barber_panel.html", context)


class BarberScheduleView(View):
    def get(self, request, barber_id):
        barber = BarberProfile.objects.get(pk=barber_id)
        timerange = TimeRange.objects.filter(barber=barber)
        saturday = timerange.filter(Days=0)
        sunday = timerange.filter(Days=1)
        monday = timerange.filter(Days=2)
        tuesday = timerange.filter(Days=3)
        wednesday = timerange.filter(Days=4)
        thursday = timerange.filter(Days=5)
        friday = timerange.filter(Days=6)

        context = {
            "barber": barber,
            "timerange": timerange,
            "saturday": saturday,
            "sunday": sunday,
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday,
        }
        return render(request, "barbers/barber_schedule.html", context)
