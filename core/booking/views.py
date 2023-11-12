from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

# local
from .models import Booking, TimeRange
from .utils import TimeSlotgenerator, Dateslotgenerator
from .forms import BookingForm
from accounts.models import BarberProfile

from django.shortcuts import get_object_or_404


def booking_test(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)

    all_time_ranges = TimeRange.objects.filter(barber=barber).order_by("Days")
    all_week_slot_time = []

    all_date_exist = Dateslotgenerator()  # all date that exist
    all_date_exist = Paginator(all_date_exist, 15)

    try:
        page_number = request.GET.get("page")
        all_date_exist = all_date_exist.get_page(page_number)

    except PageNotAnInteger:
        all_date_exist = all_date_exist.get_page(1)

    except EmptyPage:
        all_date_exist = all_date_exist.get_page(1)

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
            "all_date_exist": all_date_exist,
            "barber": barber,
        },
    )


######################################################
def booking_test2(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)

    all_time_ranges = TimeRange.objects.filter(barber=barber).order_by("Days")
    all_week_slot_time = []

    all_date_exist = (
        Dateslotgenerator()
    )  # Replace with your code to get available dates
    all_date_exist = Paginator(all_date_exist, 7)

    try:
        page_number = request.GET.get("page")
        all_date_exist = all_date_exist.get_page(page_number)

    except PageNotAnInteger:
        all_date_exist = all_date_exist.get_page(1)

    except EmptyPage:
        all_date_exist = all_date_exist.get_page(1)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create a new Booking instance with the form data
            new_booking = form.save(commit=False)
            new_booking.customer = request.user
            new_booking.barber = "s"
            new_booking.selected_slot = request.POST.get("selected_slot")
            new_booking.selected_date = request.POST.get("selected_date")
            new_booking.save()  # Save the instance to the database
            return redirect("success_page")  # Redirect to a success page
    else:
        form = BookingForm()

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
            "form": form,
            "barber": barber,
        },
    )


#########################################################################


class BookingListView(ListView):
    model = Booking
    template_name = "booking/booking_list.html"
    context_object_name = "bookings"


class AdminCalendarView(TemplateView):
    template_name = "booking/schedule-timings.html"
