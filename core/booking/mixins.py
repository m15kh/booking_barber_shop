from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class BookingPermissionMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "customerprofile"):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )
        return super().dispatch(request, *args, **kwargs)
