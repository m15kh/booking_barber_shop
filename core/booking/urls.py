from django.urls import path
from .views import (
    BookingListView,
    AdminCalendarView,
)
from .views import (
    BookingDateView,
    booking_time,
    booking_success,
)

app_name = "booking"

urlpatterns = [
    path(
        "bookingdate/<int:barber_id>/", BookingDateView.as_view(), name="booking_date"
    ),
    path("bookingtime/<int:barber_id>/", booking_time, name="booking_time"),
    path("booking_success", booking_success, name="booking_success"),
    path("", BookingListView.as_view(), name="booking_list"),
    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
