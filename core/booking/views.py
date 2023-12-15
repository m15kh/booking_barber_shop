from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# local
from .models import Booking, TimeRange, ExcludedDates
from .utils import TimeSlotgenerator, Dateslotgenerator
from accounts.models import BarberProfile, CustomerProfile
from .forms import BookingForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404

# 3rd party
from datetime import datetime, date
from django.views import View


class BookingDateView(View):
    def get(self, request, barber_id):
        barber = get_object_or_404(BarberProfile, id=barber_id)
        check_timerange_day_exist = TimeRange.objects.filter(barber=barber)
        # Assuming check_timerange_day_exist is your QuerySet
        day_names_list = [
            str(timerange).strip() for timerange in check_timerange_day_exist
        ]

        # Given list of days
        days_list = day_names_list
        print("Days in the list:", days_list)
        # All days of the week
        all_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        missing_days = set(all_days) - set(days_list)
        missing_days_list = list(missing_days)
        print("Days not in the list:", missing_days_list)

        exclude_dates = ExcludedDates.objects.filter(
            barber=barber, date__gte=date.today()
        )
        exclude_dates_list = [
            exclude_date.date.strftime("%Y-%m-%d") for exclude_date in exclude_dates
        ]

        all_dateslot = Dateslotgenerator(
            exclude_namedays=missing_days_list, exclude_dates=exclude_dates_list
        )
        return render(
            request,
            "booking/booking_date.html",
            {
                "all_dateslot": all_dateslot,
                "barber": barber,
            },
        )


class BookingTimeView(LoginRequiredMixin, View):
    template_name = "booking/booking_time.html"

    days_converter = {
        "Saturday": 0,
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6,
    }

    def get(self, request, barber_id):
        barber = get_object_or_404(BarberProfile, id=barber_id)
        return render(request, self.template_name, {"barber": barber})

    def post(self, request, barber_id):
        selected_date = request.POST.get("selected_date")
        date_object = datetime.strptime(selected_date, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")

        barber = get_object_or_404(BarberProfile, id=barber_id)

        timeslot_step = TimeRange.objects.filter(
            barber=barber, Days=self.days_converter[day_of_week]
        )

        reserve_timeslot = Booking.objects.filter(barber=barber, date=selected_date)

        all_reserve = [booking.time.strftime("%H:%M") for booking in reserve_timeslot]

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

        return render(
            request,
            self.template_name,
            {
                "barber": barber,
                "selected_date": selected_date,
                "day_of_week": day_of_week,
                "all_timeslot": all_timeslot,
                "all_reserve": all_reserve,
            },
        )


def is_not_admin(user):
    return not user.is_staff

@user_passes_test(is_not_admin)
def your_view(request):
    # Your view logic here
    if request.user.profile:
        customer = request.user.profile
        # Rest of your view logic using the customer variable
    else:
        # Handle the case where the user does not have a profile
        customer = None
    # Rest of your view logic


class BookingSuccessView(LoginRequiredMixin, View):
    template_name = "booking/booking_success.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = BookingForm(request.POST)

        if form.is_valid():
            customer = request.user.customerprofile
            print("#############", customer)
            barber_id = request.POST.get("barber")
            print("#############", barber_id)

            timeslot = request.POST.get("timeslot")
            date = request.POST.get("date")

            barber = get_object_or_404(BarberProfile, id=barber_id)

            new_booking = form.save(commit=False)
            new_booking.customer = customer
            new_booking.barber = barber
            new_booking.slottime = request.POST.get("slottime")
            new_booking.date = request.POST.get("date")
            new_booking.save()

            return render(
                request,
                self.template_name,
                {
                    "customer": customer,
                    "barber": barber,
                    "timeslot": timeslot,
                    "date": date,
                },
            )
        else:
            print("Form is not valid")
            print(form.errors)

        return render(request, self.template_name)


class BookingListView(ListView):
    model = Booking
    template_name = "booking/booking_list.html"
    context_object_name = "bookings"


class AdminCalendarView(TemplateView):
    template_name = "booking/schedule-timings.html"
