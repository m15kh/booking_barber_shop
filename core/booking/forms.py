from django import forms
from django.core.exceptions import ValidationError
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["date", "time", "barber"]
        
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop("customer", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        barber = cleaned_data.get("barber")
        # if Booking.objects.filter(date = date,customer=self.customer,barber=barber).exists():
        #     self.add_error(
        #         None, "This time is already booked"
        #     )  # Add the error to a non-field, can also specify a field

        return cleaned_data
