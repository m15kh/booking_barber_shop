from .models import BarberUser, CustomerUser, BarberProfile, CustomerProfile, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number", "date")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    list_display = (
        "username",
        "id",
        "last_name",
        "phone_number",
        "email",
        "is_active",
        "is_staff",
        "role",
    )
    list_filter = ("role",)
    search_fields = ("username", "role", "last_name")


@admin.register(BarberUser)
class BarberUserAdmin(UserAdmin):
    list_display = ("username", "id", "email", "first_name", "last_name", "role")
    list_filter = ("role",)
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number", "date")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


@admin.register(BarberProfile)
class BarberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "image")
    ordering = ("id",)
    readonly_fields = ("user",)  # can't change user

    def has_add_permission(self, request):  # remove add user
        return False


@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    list_display = ("username", "id", "last_name", "phone_number", "email", "role")
    list_filter = ("role",)
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number", "date")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    ordering = ("id",)
    readonly_fields = ("user",)  # can't change user

    def has_add_permission(self, request):  # remove add user
        return False
