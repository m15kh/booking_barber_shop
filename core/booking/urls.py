from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentListView_main,
    CurrentWeekCalendarView,
    AdminCalendarView,
)

app_name = "booking"

urlpatterns = [
    path("", AppointmentListView.as_view(), name="appointment-list"),
    path("main", AppointmentListView_main.as_view(), name="appointment-list-main"),
    path(
        "current-week/", CurrentWeekCalendarView.as_view(), name="current_week_calendar"
    ),
    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
