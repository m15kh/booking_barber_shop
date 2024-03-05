from accounts.models import BarberProfile
from django.views.generic import TemplateView, ListView
from accounts.models import BarberUser, User,  CustomerUser , BarberProfile
from django.views import View
from django.shortcuts import render
class HomePageView(View):
    def get(self, request):
        barbers = BarberProfile.objects.all()
        return render(request, "pages/home.html", {"barbers": barbers})


class TestPageView(TemplateView):
    template_name = "pages/test.html"


class ListBarberPageView(ListView):
    model = BarberProfile
    template_name = "pages/list_barber.html"
    context_object_name = "barbers"


class ComponentPageView(TemplateView):
    template_name = "pages/components.html"
