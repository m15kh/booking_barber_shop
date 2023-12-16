from django.urls import path
from .views import CustomerPanelView

app_name = "customers"
urlpatterns = [path("<int:customer_id>", CustomerPanelView.as_view(), name="customer_panel")]
