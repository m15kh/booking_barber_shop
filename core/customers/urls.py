from django.urls import path
from .views import CustomerPanelView, InvoiceDetailsView

app_name = "customers"
urlpatterns = [
    path("<int:customer_id>", CustomerPanelView.as_view(), name="customer_panel"),
    path(
        "invoice_details",
        InvoiceDetailsView.as_view(),
        name="invoice_details",
    ),
]
