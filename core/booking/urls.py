from django.urls import path

from .views import (
    BookingDateView,
    BookingTimeView,
    BookingSuccessView,
)

app_name = "booking"

urlpatterns = [
    path(
        "<int:barber_id>/", BookingDateView.as_view(), name="booking_date"
    ),
    path(
        "<int:barber_id>/time", BookingTimeView.as_view(), name="booking_time"
    ),
    path("booking_success", BookingSuccessView.as_view(), name="booking_success"),
]
