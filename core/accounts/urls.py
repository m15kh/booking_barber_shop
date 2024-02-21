from django.urls import path
from .views import SignUpView
from .views import ChangePasswordView, PasswordChangedView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-changed/', PasswordChangedView.as_view(), name='password_changed'),
]
