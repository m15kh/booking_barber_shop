from django.views.generic import ListView, TemplateView
from .models import Appointment
from datetime import datetime, timedelta


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'booking/appointment_list.html'
    context_object_name = 'appointments'


class AppointmentListView_main(ListView):
    model = Appointment
    template_name = 'booking/main.html'
    context_object_name = 'appointments'



class CurrentWeekCalendarView(ListView):
    template_name = 'booking/calendar.html'
    context_object_name = 'current_week_dates'

    def get_queryset(self):
        # Get today's date
        today = datetime.now()

        # Calculate the start and end dates of the current week
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Generate a list of dates for the current week
        current_week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

        return current_week_dates

class AdminCalendarView(TemplateView):
    template_name = 'booking/schedule-timings.html'
    
