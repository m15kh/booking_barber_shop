from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# local
from .models import BarberUser, CustomerUser, BarberProfile, CustomerProfile, User


class BarberProfileInline(admin.StackedInline):
    model = BarberProfile
    can_delete = False


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False


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

    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == "BARBERUSER":
            return [BarberProfileInline(self.model, self.admin_site)]
        elif obj and obj.role == "CUSTOMERUSER":
            return [CustomerProfileInline(self.model, self.admin_site)]
        else:
            return super().get_inline_instances(request, obj)


@admin.register(BarberUser)
class BarberUserAdmin(UserAdmin):
    inlines = (BarberProfileInline,)
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


@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    inlines = (CustomerProfileInline,)
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
