from django.urls import path
from .views import RegisterView
from .views import (
    ChangePasswordView,
    PasswordChangedView,
    UserRegisterVerifyCodeView,
    UserLoginView,
    UserLogoutView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("password-changed/", PasswordChangedView.as_view(), name="password_changed"),
    path("verify/", UserRegisterVerifyCodeView.as_view(), name="verify_code"),
    path(
        "forget-password/", UserRegisterVerifyCodeView.as_view(), name="forget_password"
    ),
]
