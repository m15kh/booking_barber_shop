from django.urls import path
from .views import (
    BookingListView,
    AdminCalendarView,
)
from .views import (
    BookingDateView,
    BookingTimeView,
    BookingSuccessView,
)

app_name = "booking"

urlpatterns = [
    path(
        "bookingdate/<int:barber_id>/", BookingDateView.as_view(), name="booking_date"
    ),
    path(
        "bookingtime/<int:barber_id>/", BookingTimeView.as_view(), name="booking_time"
    ),
    path("booking_success", BookingSuccessView.as_view(), name="booking_success"),
    path("", BookingListView.as_view(), name="booking_list"),
    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
