# mixins.py
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BarberProfilePermissionMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Ensure that the user has a related BarberProfile
        if not hasattr(request.user, "barberprofile"):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        # Check if the requested barber_id matches the user's BarberProfile
        barber_id = kwargs.get("barber_id")
        if request.user.barberprofile.id != int(barber_id):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        return super().dispatch(request, *args, **kwargs)
