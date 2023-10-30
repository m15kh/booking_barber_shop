from django.views.generic import ListView, TemplateView
from django.shortcuts import render

#local
from .models import Booking , TimeRange
from .utils import TimeSlotgenerator ,Dateslotgenerator

def booking_test(request):
    all_time_ranges = TimeRange.objects.all().order_by('Days')

    
    all_week_slot_time  = []

    all_date_exist = Dateslotgenerator() # all date that exist

    for timerange in all_time_ranges:

        time_slots = TimeSlotgenerator(
            timerange.workstart.strftime('%H:%M'),
            timerange.workfinish.strftime('%H:%M'),
            timerange.reststart.strftime('%H:%M'),
            timerange.restfinish.strftime('%H:%M'),
            timerange.duration,
        )
        all_week_slot_time.append({'timerange': timerange, 'time_slots': time_slots})


   

    return render(request, 'booking/booking_test.html', {'all_week_slot_time': all_week_slot_time, 'all_date_exist': all_date_exist})

def booking_test2(request):
    dateslots = Dateslotgenerator()
    return render(request, 'booking/booking_test2.html', {'dateslots': dateslots})



class BookingListView(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'


class AdminCalendarView(TemplateView):
    template_name = 'booking/schedule-timings.html'
    
