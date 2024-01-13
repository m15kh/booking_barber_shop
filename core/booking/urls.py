from django.urls import path

from .views import (
    BookingDateView,
    BookingTimeView,
    BookingSuccessView,
    BookingProccessView,
)

app_name = "booking"

urlpatterns = [
    path("<int:barber_id>/", BookingDateView.as_view(), name="booking_date"),
    path("<int:barber_id>/time/", BookingTimeView.as_view(), name="booking_time"),
    path("booking_proccessing", BookingProccessView.as_view(), name="booking_process"),
    path(
        "booking_success/<int:barber_id>/<str:date>/<str:time>/",
        BookingSuccessView.as_view(),
        name="booking_success",
    ),
]
