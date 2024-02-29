from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from .models import (
    BarberUser,
    CustomerUser,
    BarberProfile,
    CustomerProfile,
    User,
    OtpCode,
)

from django.contrib import admin
from .models import User

admin.site.register(User)
admin.site.register(BarberUser)
admin.site.register(CustomerUser)

admin.site.register(OtpCode)