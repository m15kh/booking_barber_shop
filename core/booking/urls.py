from django.urls import path
from .views import (
    BookingListView,
    AdminCalendarView,
)
from .views import (
    booking_test,
    booking_date,
    booking_time,
    booking_success,
)

app_name = "booking"

urlpatterns = [
    path("bookingtest/<int:barber_id>/", booking_test, name="booking_test"),
    path("bookingtest2/<int:barber_id>/", booking_date, name="booking_date"),
    path("bookingtest3/<int:barber_id>/", booking_time, name="booking_time"),
    path("booking_success", booking_success, name="booking_success"),
    path("", BookingListView.as_view(), name="booking_list"),
    path("schedule", AdminCalendarView.as_view(), name="doctor_schedule"),
]
