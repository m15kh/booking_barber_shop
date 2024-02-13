from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin


# local
from .models import BarberUser, CustomerUser, BarberProfile, CustomerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        if request.user.role == "ADMIN":
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.role == "ADMIN":
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.role == "ADMIN":
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role="ADMIN")

    def save_model(self, request, obj, form, change):
        obj.role = "ADMIN"
        obj.is_staff = True
        obj.is_superuser = True
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if request.user.role == "BARBERUSER":
            perms.clear()
        return perms
    
    def has_delete_permission(self, request, obj=None): #admin can'y delete himself
        if request.user == obj:
            return False
        return True

    readonly_fields = ("last_login", "date_joined", 'role', 'is_staff', 'is_superuser')    

    fieldsets = (
        (None, {"fields": ("username", "password", "role")}),
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
        "last_name",
        "phone_number",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
    )
    list_filter = ("is_active", )


class CustomUserAdmin(BaseUserAdmin):
    def has_module_permission(self, request):
        return request.user.role == "ADMIN" or request.user.role == "BARBERUSER"

    def has_add_permission(self, request):
        if request.user.role == "ADMIN":
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.role == "ADMIN":
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.role == "ADMIN":
            return True

    inlines = []
    list_display = ()
    list_filter = ()
    search_fields = ()
    fieldsets = ()
    readonly_fields = ()


class BarberProfileInline(admin.StackedInline):
    model = BarberProfile
    can_delete = False


@admin.register(BarberUser)
class BarberUserAdmin(CustomUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "BARBERUSER":
            return qs.filter(pk=request.user.pk)
        elif request.user.role == "ADMIN":
            return qs.all()
        else:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.role == "ADMIN"

    def has_add_permission(self, request):
        return request.user.role == "ADMIN"

    def has_module_permission(self, request):
        return True

    inlines = (BarberProfileInline,)
    list_display = (
        "username",
        "phone_number",
        "last_name",
        "role",
        "is_active",
        "is_superuser",
        "is_staff",
        "role",
    )

    readonly_fields = ("role", "last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("username", "password", "role")}),
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
        (
            "groups",
            {
                "fields": ("groups",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.role == "ADMIN":
            return readonly_fields
        return readonly_fields + (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False


@admin.register(CustomerUser)
class CustomerUserAdmin(CustomUserAdmin):

    inlines = (CustomerProfileInline,)
    list_display = (
        "username",
        "phone_number",
        "last_name",
        "email",
        "is_active",
        "role",
    )    
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
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    readonly_fields = ("is_staff", "is_superuser", "last_login", "date_joined")

    search_fields = ("phone_number",)



admin.site.unregister(Group)


class CustomGroupAdmin(BaseGroupAdmin):
    def has_module_permission(self, request):
        return request.user.role == "ADMIN"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "ADMIN":
            return qs
        else:
            return qs.none()


@admin.register(Group)
class GroupAdmin(CustomGroupAdmin):
    pass
