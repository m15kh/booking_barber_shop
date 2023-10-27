from django.views.generic import ListView, TemplateView
from django.shortcuts import render

#local
from .models import Booking , TimeRange
from .utils import TimeSlotgenerator

def booking_test(request):
    all_time_ranges = TimeRange.objects.all()
    processed_data = []

    for timerange in all_time_ranges:
        time_slots = TimeSlotgenerator(
            timerange.start_hour.strftime('%H:%M'),
            timerange.end_hour.strftime('%H:%M'),
            timerange.start_rest_hour.strftime('%H:%M'),
            timerange.finish_rest_hour.strftime('%H:%M')
        )
        processed_data.append({'appointment_hour': timerange, 'time_slots': time_slots})

    return render(request, 'booking/booking_test.html', {'processed_data': processed_data})



class BookingListView(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'


class AdminCalendarView(TemplateView):
    template_name = 'booking/schedule-timings.html'
    
