from django.urls import path
from .views import AppointmentListView

app_name = 'booking'

urlpatterns = [
     path('', AppointmentListView.as_view(), name='appointment-list'),

]
