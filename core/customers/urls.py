from django.urls import path
from .views import CustomerPanelView

urlpatterns = [path("<int:customer_id>", CustomerPanelView.as_view(), name="customer_panel")]
