from django.views import View
from django.shortcuts import render
from accounts.models import CustomerProfile
from booking.models import Booking
from .mixins import CustomerProfilePermissionMixin

# 3rth party
from datetime import date


class CustomerPanelView(CustomerProfilePermissionMixin, View):
    def get(self, request, customer_id):
        customer = CustomerProfile.objects.get(pk=customer_id)
        bookings = Booking.objects.filter(customer=customer)
        today = date.today()

        active_bookings = bookings.filter(
            status=True, customer=customer, date__gte=today
        )
        deactived_bookings = bookings.filter(
            status=False, customer=customer, date__gte=today
        )

        context = {
            "customer": customer,
            "bookings": bookings,
            "active_bookings": active_bookings,
            "deactive_bookings": deactived_bookings,
        }

        return render(request, "customers/customer_panel.html", context)


class CustomerEditProfile(CustomerProfilePermissionMixin, View):
    def get(self, request, customer_id):
        customer = CustomerProfile.objects.get(pk=customer_id)
        context = {"customer": customer}
        return render(request, "customers/cus_editprofile.html", context)


class CustomerChangePassword(CustomerProfilePermissionMixin, View):
    def get(self, request, customer_id):
        customer = CustomerProfile.objects.get(pk=customer_id)
        context = {"customer": customer}
        return render(request, "customers/cus_change_password.html", context)

class InvoiceDetailsView(View):
    def get(self, request):
        info_booking = Booking.objects.filter(customer=request.user.customerprofile)

        return render(request, "customers/invoice_details.html")
