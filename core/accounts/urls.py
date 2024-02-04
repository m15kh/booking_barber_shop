from django.urls import path
from .views import SignUpView
from .views import PasswordChangeView, PasswordResetDoneView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password-change", PasswordChangeView.as_view(), name="password-change-view"),
    path(
        "change-password/done/",
        PasswordResetDoneView.as_view(),
        name="password-reset-done-view",
    ),
]
