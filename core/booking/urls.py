from django.urls import path
from .views import (
    BookingListView,
    AdminCalendarView,
)
from .views import booking_test, booking_test2, booking_test3

app_name = "booking"

urlpatterns = [
    path("bookingtest/<int:barber_id>/", booking_test, name="booking_test"),
    path("bookingtest2/<int:barber_id>/", booking_test2, name="booking_test2"),
    path("bookingtest3/<int:barber_id>/", booking_test3, name="booking_test3"),
    path("", BookingListView.as_view(), name="booking_list"),
    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
