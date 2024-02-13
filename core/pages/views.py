from accounts.models import BarberProfile
from django.views.generic import TemplateView, ListView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class TestPageView(TemplateView):
    template_name = "pages/test.html"


class ListBarberPageView(ListView):
    model = BarberProfile
    template_name = "pages/list_barber.html"
    context_object_name = "barbers"


class ComponentPageView(TemplateView):
    template_name = "pages/components.html"
