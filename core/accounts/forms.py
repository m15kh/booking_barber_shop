# forms.py
from django import forms
from .models import User, OtpCode, CustomerUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator  # Import RegexValidator from django.core.validators


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(
        label="Repeat New Password", widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        repeat_new_password = cleaned_data.get("repeat_new_password")

        if new_password != repeat_new_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(
        required=True,  # Ensures the field is not null
        validators=[
            RegexValidator(r"^\d{11}$", "Enter a valid 11-digit phone number.")
        ],
    )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']

        user = CustomerUser.objects.filter(username=phone).exists()
        if user:
            raise ValidationError('This phone number already exists')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class verifyCodeForm(forms.Form):
    code = forms.IntegerField(required=True)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code:
            raise forms.ValidationError("Code field cannot be empty.")

        return code
