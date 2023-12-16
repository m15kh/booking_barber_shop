from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CustomerProfilePermissionMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "customerprofile"):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )
        customer_id = kwargs.get("customer_id")
        if request.user.customerprofile.id != int(customer_id):
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )


        return super().dispatch(request,*args, **kwargs)