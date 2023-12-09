from django.views.generic import ListView, TemplateView
from django.shortcuts import render

# local
from .models import Booking, TimeRange
from .utils import TimeSlotgenerator, Dateslotgenerator
from accounts.models import BarberProfile, CustomerProfile
from .forms import BookingForm

from django.shortcuts import get_object_or_404

# 3rd party
from datetime import datetime
from django.views import View


class BookingDateView(View):
    def get(self, request, barber_id):
        barber = get_object_or_404(BarberProfile, id=barber_id)
        all_dateslot = Dateslotgenerator()
        return render(
            request,
            "booking/booking_date.html",
            {
                "all_dateslot": all_dateslot,
                "barber": barber,
            },
        )


def booking_time(request, barber_id):
    days_convertor = {
        "Saturday": 0,
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6,
    }

    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        print(selected_date)
        date_object = datetime.strptime(selected_date, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")
        print(day_of_week)

    barber = get_object_or_404(BarberProfile, id=barber_id)

    timeslot_step = TimeRange.objects.filter(
        barber=barber, Days=days_convertor[day_of_week]
    )

    reserve_timeslot = Booking.objects.filter(
        barber=barber, date=selected_date
    )  # return all time that reserved

    # Extract the timeslot values from each Booking instance
    all_reserve = [booking.timeslot.strftime("%H:%M") for booking in reserve_timeslot]
    print("all_reserve", all_reserve)

    print(timeslot_step)

    if timeslot_step.exists():
        first_timeslot = timeslot_step.first()

        all_timeslot = TimeSlotgenerator(
            first_timeslot.workstart.strftime("%H:%M"),
            first_timeslot.workfinish.strftime("%H:%M"),
            first_timeslot.reststart.strftime("%H:%M"),
            first_timeslot.restfinish.strftime("%H:%M"),
            first_timeslot.duration,
        )
    else:
        print("No timeslots found for the specified conditions.")

    print("all_timeslot", all_timeslot)

    return render(
        request,
        "booking/booking_time.html",
        {
            "barber": barber,
            "selected_date": selected_date,
            "day_of_week": day_of_week,
            "all_timeslot": all_timeslot,
            "all_reserve": all_reserve,
        },
    )


def booking_success(request):
    if request.method == "POST":
        print(request.POST)
    form = BookingForm(request.POST)

    if form.is_valid():
        customer = request.user
        barber = request.POST.get("barber")
        timeslot = request.POST.get("timeslot")
        date = request.POST.get("date")
        print("valid")

        barber = get_object_or_404(BarberProfile, id=barber)

        print(customer, barber, timeslot, date)
        new_booking = form.save(commit=False)
        new_booking.customer = request.user
        barber = request.POST.get("barber")
        barber = get_object_or_404(BarberProfile, id=barber)
        new_booking.barber = barber
        new_booking.slottime = request.POST.get("slottime")
        new_booking.date = request.POST.get("date")
        new_booking.save()
        # return redirect("success_page")  # Redirect to a success page

    else:
        print("fuck")
        print(form.errors)

    return render(
        request,
        "booking/booking_success.html",
        {
            "customer": customer,
            "barber": barber,
            "timeslot": timeslot,
            "date": date,
        },
    )


class BookingListView(ListView):
    model = Booking
    template_name = "booking/booking_list.html"
    context_object_name = "bookings"


class AdminCalendarView(TemplateView):
    template_name = "booking/schedule-timings.html"
