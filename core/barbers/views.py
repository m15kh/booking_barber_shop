from django.views import View
from django.shortcuts import render
from accounts.models import BarberProfile
from booking.models import Booking
from datetime import datetime, timedelta


class BarberPanelView(View):
    def get(self, request, barber_id):
        barber = BarberProfile.objects.get(pk=barber_id)
        tomorrow_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        upcoming_bookings = Booking.objects.filter(
            barber=barber,
            date__gte=tomorrow_date,
        ).order_by("date", "time")
        count_tommorrow_bookings = upcoming_bookings.count()

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
            "count_tommorrow_bookings": count_tommorrow_bookings,
        }
        return render(request, "barbers/barber_panel.html", context)
