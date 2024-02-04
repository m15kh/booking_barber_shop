from django.urls import path
from .views import (
    CustomerPanelView,
    InvoiceDetailsView,
    CustomerEditProfile,
    CustomerChangePassword,
)

app_name = "customers"
urlpatterns = [
    path("<int:customer_id>", CustomerPanelView.as_view(), name="customer_panel"),
    path(
        "invoice-details",
        InvoiceDetailsView.as_view(),
        name="invoice_details",
    ),
    path(
        "<int:customer_id>/editprofile",
        CustomerEditProfile.as_view(),
        name="edit_profile",
    ),
    path(
        "<int:customer_id>/change-password",
        CustomerChangePassword.as_view(),
        name="change_password",
    ),
]
