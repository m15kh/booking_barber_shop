from django.urls import path
from .views import BarberPanelView

app_name = "barbers"
urlpatterns = [path("<int:barber_id>", BarberPanelView.as_view(), name="barber_panel")]
