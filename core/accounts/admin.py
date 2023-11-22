from django.contrib import admin
from .models import Barber, Customer, BarberProfile, CustomerProfile


# Custom admin class for Barber model
class BarberAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role")
    list_filter = ("role",)
    search_fields = ("username", "email", "first_name", "last_name")


# Custom admin class for Customer model
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    list_filter = ("role",)
    search_fields = ("username", "email", "first_name", "last_name")


class BarberProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', "image",)

    ordering = ('id',)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', "phone_number",)


# Register the custom admin classes for your models
admin.site.register(Barber, BarberAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BarberProfile, BarberProfileAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
