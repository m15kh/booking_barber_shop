from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ChangePasswordForm 
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User
from django.shortcuts import render


class SignUpView(CreateView):
    pass


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("pages:home")
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            print("%%%%%%%%%%%%%%%%", form)
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            print("new password", new_password)
            print("old password", old_password)

            user = request.user

            if not check_password(old_password, user.password):
                messages.error(request, "Old password is incorrect.")
                form.add_error("old_password", "Old password is incorrect.")
                return self.form_invalid(form)

            user.set_password(new_password)
            user.save()

            messages.success(request, "Password changed successfully.")
            return self.form_valid(form)
        else:

            return self.form_invalid(form)


class PasswordChangedView(TemplateView):
    template_name = "pages/home.html"


