from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from .models import BarberUser, CustomerUser, BarberProfile, CustomerProfile, User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # functions
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

    list_display = (
        "phone_number",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
    )

    readonly_fields = ("last_login", "date_joined", 'role')    
    ordering = ('last_name',)
    list_filter = ("is_active",)

    fieldsets = (
        (None, {"fields": ("password", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    'is_staff',
                    'is_superuser',
                    "last_login",
                    "date_joined",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "birthday")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


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

from django.contrib import admin
from .models import BarberProfile, BarberUser


class BarberProfileInline(admin.StackedInline):
    model = BarberProfile
    can_delete = False


@admin.register(BarberUser)
class BarberUserAdmin(CustomUserAdmin):
    inlines = (BarberProfileInline,)  

    def get_inline_instances(self, request, obj=None):
        if obj:  # Editing an existing object
            return super().get_inline_instances(request, obj)
        return []

    # Define other methods and attributes as you've implemented before

    list_display = (
        "phone_number",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
    )

    readonly_fields = ("last_login", "date_joined", "role")
    ordering = ("last_name",)
    list_filter = ("is_active",)

    fieldsets = (
        (None, {"fields": ("password", "role")}),
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
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "birthday")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False


@admin.register(CustomerUser)
class CustomerUserAdmin(CustomUserAdmin):

    inlines = (CustomerProfileInline,)
    def get_inline_instances(self, request, obj=None):
        if obj:  # Editing an existing object
            return super().get_inline_instances(request, obj)
        return []

    list_display = (
        "phone_number",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "role",
    )

    readonly_fields = ("last_login", "date_joined", "role")
    ordering = ("last_name",)
    list_filter = ("is_active",)

    fieldsets = (
        (None, {"fields": ( "password", "role")}),
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
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "birthday")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

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
