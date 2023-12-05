from django.views import View
from django.shortcuts import render
from accounts.models import CustomerProfile
from booking.models import Booking


class CustomerPanelView(View):
    def get(self, request, customer_id):
        customer = CustomerProfile.objects.get(pk=customer_id)
        bookings = Booking.objects.filter(customer=customer)

        context = {
            "customer": customer,
            "bookings": bookings,
        }

        return render(
            request, "customers/customer_panel.html", context
        )
