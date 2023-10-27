from django.urls import path
from .views import (
    BookingListView,
    AdminCalendarView,
)
from .views import booking_test

app_name = "booking"

urlpatterns = [
    path("bookingtest", booking_test , name="booking_test"),
    path("", BookingListView.as_view(), name="booking_list"),


    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
