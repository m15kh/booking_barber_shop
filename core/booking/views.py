from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse

# local
from .models import Booking, TimeRange, ExcludedDates
from .utils import TimeSlotgenerator, Dateslotgenerator
from accounts.models import BarberProfile
from .forms import BookingForm
from .mixins import BookingPermissionMixin

# 3rd party
from datetime import datetime
from datetime import date as datee


days_converter = {
    "Saturday": 0,
    "Sunday": 1,
    "Monday": 2,
    "Tuesday": 3,
    "Wednesday": 4,
    "Thursday": 5,
    "Friday": 6,
}


class BookingDateView(BookingPermissionMixin, View):
    def get(self, request, barber_id):
        barber = get_object_or_404(BarberProfile, id=barber_id)
        check_timerange_day_exist = TimeRange.objects.filter(barber=barber)
        # Assuming check_timerange_day_exist is your QuerySet
        day_names_list = [
            str(timerange).strip() for timerange in check_timerange_day_exist
        ]
        # print("Days in the list:", day_names_list)
        all_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        missing_days = set(all_days) - set(day_names_list)
        missing_days_list = list(missing_days)  # Days not in the list:
        # print("Days not in the list:", missing_days_list)

        exclude_dates = (
            ExcludedDates.objects.filter(  # days that barber  is not available
                barber=barber, date__gte=datee.today()
            )
        )
        exclude_dates_list = [
            exclude_date.date.strftime("%Y-%m-%d") for exclude_date in exclude_dates
        ]

        all_available_dates = Dateslotgenerator(  # return all available dates
            exclude_namedays=missing_days_list, exclude_dates=exclude_dates_list
        )
        # check that date is full timeslot  or not

        barber_timerange = TimeRange.objects.filter(barber=barber)
        info_dict = {}

        for i in barber_timerange:
            info_dict[i.get_day_name()] = i.number_timeslots

        # Print the dictionary
        print('asa',info_dict)

                        

        full_date  = []
        for date in all_available_dates:  # all_da
            date = date[0]
            date_deform = date.strftime("%Y-%m-%d")  # Convert datetime.date to string
            date_name = date.strftime("%A")
            count_active_reserve = Booking.objects.filter(
                barber=barber, date=date_deform
            ).count()

            if date_name in info_dict:
                print('yreee________________--------------_____')
                print(count_active_reserve , info_dict[date_name],'--------------')
                if count_active_reserve  == info_dict[date_name]:
                    full_date.append(date_deform)
                    
        print("Full date:", full_date)
        return render(
            request,
            "booking/booking_date.html",
            {
                "all_dateslot": all_available_dates,
                'full_date':full_date,
                "barber": barber,
            },
        )


class BookingTimeView(BookingPermissionMixin, View):
    template_name = "booking/booking_time.html"

    def post(self, request, barber_id):
        date = request.POST.get("selected_date")
        date_format = datetime.strptime(
            date, "%Y-%m-%d"
        )  # change format of date to valid format (str)
        name_of_day = date_format.strftime("%A")  # retuen for a example friday

        barber = get_object_or_404(BarberProfile, id=barber_id)

        timeslots_selected_date = TimeRange.objects.filter(  # retuen all range timeslot for day that selected ( for a example show time slot for tuesday )
            barber=barber,
            Days=days_converter[name_of_day],  # Days=self.days_converter[name_of_day]
        )
        reserved_timeslot = Booking.objects.filter(
            barber=barber, date=date
        )  # return all query for reserved timeslot

        reserved_timeslot_format = [
            booking.time.strftime("%H:%M") for booking in reserved_timeslot
        ]  # reformat  return all query for reserved timeslot

        if timeslots_selected_date.exists():
            first_timeslot = timeslots_selected_date.first()

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
                "selected_date": date,
                "day_of_week": name_of_day,
                "all_timeslot": all_timeslot[0],
                "all_reserve": reserved_timeslot_format,
            },
        )


class BookingSuccessView(BookingPermissionMixin, View):
    template_name = "booking/booking_success.html"

    def post(self, request):
        form = BookingForm(request.POST, customer=request.user.customerprofile)

        if form.is_valid():
            customer = request.user.customerprofile
            barber_id = request.POST.get("barber")
            barber = get_object_or_404(BarberProfile, id=barber_id)
            time = request.POST.get("time")
            date = request.POST.get("date")
            # start save booking
            new_booking = form.save(commit=False)
            new_booking.customer = customer
            new_booking.barber = barber
            new_booking.time = time
            new_booking.date = date
            new_booking.save()
            messages.success(
                request, "you reserved appointment successfully", "success"
            )
            return render(
                request,
                self.template_name,
                {
                    "customer": customer,
                    "barber": barber,
                    "time": time,
                    "date": date,
                },
            )

        else:
            messages.error(
                request,
                "you have active reservation with this barber on this  date ",
                "danger",
            )
            barber_id = request.POST.get("barber")
            print(request.path)
        return redirect(
            reverse("booking:booking_date", kwargs={"barber_id": barber_id})
        )
