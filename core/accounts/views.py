from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ChangePasswordForm 
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate

# local
from .models import OtpCode
from .forms import UserRegisterForm, verifyCodeForm, UserLoginForm
from .models import CustomerUser
from utils import sent_otp_code

# 3rd party
import random


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd["phone_number"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You logged in successfully.", "info")
                return redirect("pages:home")
            else:
                # Display error message if authentication fails
                form.add_error(None, "Phone number or password is incorrect.")
                messages.error(
                    request, "Phone number or password is incorrect.", "warning"
                )
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", "success")
        return redirect("pages:home")


class RegisterView(View):
    template_name = "accounts/register.html"
    success_url = reverse_lazy("pages:home")
    form_class = UserRegisterForm  

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            phone_number=form.cleaned_data["phone_number"]
            print(phone_number)

            random_code = random.randint(10000, 99999)
            sent_otp_code(form.cleaned_data["phone_number"], random_code)
            OtpCode.objects.create(
                phone_number=form.cleaned_data["phone_number"], code=random_code
            )
            
            request.session["user_registeration_form_info"] = {
                "phone_number": form.cleaned_data["phone_number"],
                "code": random_code,
            }
            
            messages.success(request, "An activation code has been sent to your phone number.", 'success')
            return redirect('accounts:verify_code')
        else:
            return render(request, self.template_name, {"form": form})


class UserRegisterVerifyCodeView(View):
    template_name = "accounts/verify_code.html"
    form_class = verifyCodeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        code_instance = OtpCode.objects.get(phone_number=request.session["user_registeration_form_info"]["phone_number"])
        created_time = code_instance.created.time()
        created_time = created_time.strftime("%H:%M:%S")
        context = {"form": form, "created_time": created_time}
        return render(
            request, self.template_name, context
        )  # Pass the form to the template context

    def post(self, request, *args, **kwargs):
        user_session = request.session["user_registeration_form_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                # create customer user
                CustomerUser.objects.create_user(
                    user_session["phone_number"],
                )

                code_instance.delete()
                messages.success(request, "you registered successfully", 'success')
                return redirect('pages:home')

            else:
                form.add_error('code', 'this code is wrong')
                messages.error(request, 'this code is wrong', 'danger')
                code_instance = OtpCode.objects.get(phone_number=request.session["user_registeration_form_info"]["phone_number"])
                created_time = code_instance.created.time()
                created_time = created_time.strftime("%H:%M:%S")
                context = {"form": form, "created_time": created_time}
                return render(
                    request, self.template_name, context
                )  # Pass the form to the template context


        else:
            return render(request, self.template_name, {"form": form})


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("pages:home")
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
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
