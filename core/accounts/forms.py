# forms.py
from django import forms
from django.contrib.auth.hashers import check_password
from .models import CustomerProfile , User

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
