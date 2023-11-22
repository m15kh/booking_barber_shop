from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect


# local
from .models import Booking, TimeRange
from .utils import TimeSlotgenerator, Dateslotgenerator
from accounts.models import BarberProfile, CustomerProfile
from .forms import BookingForm

from django.shortcuts import get_object_or_404

# 3rd party
from datetime import datetime


def booking_test(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)
    all_time_ranges = TimeRange.objects.filter(barber=barber).order_by("Days")

    if request.method == "POST":
        print("sslddf,d,dpl")
        print(request.POST)
    all_week_slot_time = []

    for timerange in all_time_ranges:
        time_slots = TimeSlotgenerator(
            timerange.workstart.strftime("%H:%M"),
            timerange.workfinish.strftime("%H:%M"),
            timerange.reststart.strftime("%H:%M"),
            timerange.restfinish.strftime("%H:%M"),
            timerange.duration,
        )
        all_week_slot_time.append({"timerange": timerange, "time_slots": time_slots})

    return render(
        request,
        "booking/booking_test.html",
        {
            "all_week_slot_time": all_week_slot_time,
            "barber": barber,
        },
    )


def booking_test2(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)

    all_time_ranges = TimeRange.objects.filter(barber=barber).order_by("Days")
    all_week_slot_time = []

    all_date_exist = (
        Dateslotgenerator()
    )  # Replace with your code to get available dates

    if request.method == "POST":
        print(request.POST)
        barber = get_object_or_404(BarberProfile, id=barber_id)

    for timerange in all_time_ranges:
        time_slots = TimeSlotgenerator(
            timerange.workstart.strftime("%H:%M"),
            timerange.workfinish.strftime("%H:%M"),
            timerange.reststart.strftime("%H:%M"),
            timerange.restfinish.strftime("%H:%M"),
            timerange.duration,
        )
        all_week_slot_time.append({"timerange": timerange, "time_slots": time_slots})

    return render(
        request,
        "booking/booking_test2.html",
        {
            "all_week_slot_time": all_week_slot_time,
            "all_date_exist": all_date_exist,
            "barber": barber,
        },
    )


def booking_test3(request, barber_id):
    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        print(selected_date)
        date_object = datetime.strptime(selected_date, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")
        print(day_of_week)

        # Use selected_date to filter available time slots for the chosen date
        # Update the following line with your code to get available time slots for the selected date

    barber = get_object_or_404(BarberProfile, id=barber_id)

    all_time_ranges = TimeRange.objects.filter(barber=barber, Days=0).order_by("Days")
    print(all_time_ranges)

    for timerange in all_time_ranges:
        time_slots = TimeSlotgenerator(
            timerange.workstart.strftime("%H:%M"),
            timerange.workfinish.strftime("%H:%M"),
            timerange.reststart.strftime("%H:%M"),
            timerange.restfinish.strftime("%H:%M"),
            timerange.duration,
        )

    return render(
        request,
        "booking/booking_test3.html",
        {
            "barber": barber,
            "selected_date": selected_date,
            "day_of_week": day_of_week,
            "time_slots": time_slots,
        },
    )


class BookingListView(ListView):
    model = Booking
    template_name = "booking/booking_list.html"
    context_object_name = "bookings"


class AdminCalendarView(TemplateView):
    template_name = "booking/schedule-timings.html"
