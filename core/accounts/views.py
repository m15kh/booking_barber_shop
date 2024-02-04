from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib.auth.views import PasswordChangeView as PasswordChangePureView
from django.contrib.auth.views import PasswordResetDoneView as PasswordResetDonePureView

from django.urls import reverse_lazy


class SignUpView(CreateView):
    pass


class PasswordChangeView(PasswordChangePureView):
    template_name = "accounts/password-change.html"
    success_url = reverse_lazy("accounts/password-reset-done-view.html")


class PasswordResetDoneView(PasswordResetDonePureView):
    template_name = "accounts/password-reset-done.html"
