from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#local
from .models import Booking , TimeRange
from .forms import BookingForm
from .utils import TimeSlotgenerator ,Dateslotgenerator

def booking_test(request):
    all_time_ranges = TimeRange.objects.all().order_by('Days')
    all_week_slot_time  = []



    all_date_exist = Dateslotgenerator() # all date that exist
    all_date_exist = Paginator(all_date_exist, 15)
    
    try:

        page_number = request.GET.get('page')
        all_date_exist = all_date_exist.get_page(page_number)

    except PageNotAnInteger:
        all_date_exist = all_date_exist.get_page(1)

    except EmptyPage:
        all_date_exist = all_date_exist.get_page(1) 

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

    all_time_ranges = TimeRange.objects.all().order_by('Days')
    all_week_slot_time = []

    all_date_exist = Dateslotgenerator()  # all dates that exist
    all_date_exist = Paginator(all_date_exist, 7)
    
    try:
        page_number = request.GET.get('page')
        all_date_exist = all_date_exist.get_page(page_number)

    except PageNotAnInteger:
        all_date_exist = all_date_exist.get_page(1)

    except EmptyPage:
        all_date_exist = all_date_exist.get_page(1) 
    


    for timerange in all_time_ranges:
        time_slots = TimeSlotgenerator(
            timerange.workstart.strftime('%H:%M'),
            timerange.workfinish.strftime('%H:%M'),
            timerange.reststart.strftime('%H:%M'),
            timerange.restfinish.strftime('%H:%M'),
            timerange.duration,
        )
        all_week_slot_time.append({'timerange': timerange, 'time_slots': time_slots})


    

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a success message here if needed
            return redirect('success_page')
    else:
        form = BookingForm()

    return render(request, 'booking/booking_test2.html', {'all_week_slot_time': all_week_slot_time, 'all_date_exist': all_date_exist, 'form': form})




class BookingListView(ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'


class AdminCalendarView(TemplateView):
    template_name = 'booking/schedule-timings.html'
    
