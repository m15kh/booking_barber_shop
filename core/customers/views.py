from django.views import View
from django.shortcuts import render
from accounts.models import CustomerProfile,User
from booking.models import Booking
from .mixins import CustomerProfilePermissionMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import EditProfileForm
# 3rth party
from datetime import date


class CustomerPanelView(View):  # CustomerProfilePermissionMixin,
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


class CustomerEditProfile(View):  # CustomerProfilePermissionMixin
    def get(self, request, customer_id):
        customer = User.objects.get(pk=customer_id)
        form = EditProfileForm(instance=customer)
        context = {"customer": customer, "form": form}
        return render(request, "customers/edit_profile.html", context)

    def post(self, request, customer_id):
        customer = User.objects.get(pk=customer_id)
        form = EditProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            print("yesssssssssssssssssssssssssssssssss it is valid")
        context = {"customer": customer, "form": form}
        return render(request, "customers/edit_profile.html", context)


class CustomerChangePassword(CustomerProfilePermissionMixin, View):
    def get(self, request, customer_id):
        customer = CustomerProfile.objects.get(pk=customer_id)
        context = {"customer": customer}
        return render(request, "customers/cus_change_password.html", context)


class InvoiceDetailsView(View):
    def get(self, request):
        info_booking = Booking.objects.filter(customer=request.user.customerprofile)

        return render(request, "customers/invoice_details.html")
