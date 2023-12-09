from django.urls import path
from .views import BarberPanelView, BarberScheduleView

app_name = "barbers"
urlpatterns = [
    path("<int:barber_id>", BarberPanelView.as_view(), name="barber_panel"),
    path(
        "<int:barber_id>/barber-schedule/",
        BarberScheduleView.as_view(),
        name="barber_schedule",
    ),
]
