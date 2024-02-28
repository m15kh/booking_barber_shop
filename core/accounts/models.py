from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

# local
from .managers import UserManager
class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        CUSTOMERUSER = "CUSTOMERUSER", "CustomerUser"
        BARBERUSER = "BARBERUSER", "BarberUser"
        ADMIN = "ADMIN", "Admin"

    base_role = Role.ADMIN

    phone_number = models.CharField(
    max_length=11,
    validators=[
        RegexValidator(r"^\d{2}$", "Enter a valid 2-digit phone number.")
    ],
    unique=True
    )
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    USERNAME_FIELD = 'phone_number'


    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)



    def __str__(self):
        return self.phone_number


class CustomerUserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMERUSER)


class CustomerUser(User):
    base_role = User.Role.CUSTOMERUSER
    customeruser = CustomerUserManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for CUSTOMERS"


class BarberUSERManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BARBERUSER)


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customerprofile"
    )
    image = models.ImageField(upload_to="customers/", default="customers/default.jpg")

    def __str__(self):
        return self.user.phone_number

    def delete(self, *args, **kwargs):
        # Delete associated BarberUser
        customer_user = CustomerProfile.objects.filter(id=self.user.id)
        if customer_user.exists():
            customer_user.delete()

        # Call the parent class delete method
        super().delete(*args, **kwargs)


class BarberUser(User):
    base_role = User.Role.BARBERUSER
    barberuser = BarberUSERManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for barbers"


class BarberProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="barberprofile"
    )
    image = models.ImageField(upload_to="barbers/", default="barbers/default.jpg")

    def __str__(self):
        return self.user.phone_number

    def delete(self, *args, **kwargs):
        # Delete associated BarberUser
        barber_user = BarberUser.objects.filter(id=self.user.id)
        if barber_user.exists():
            barber_user.delete()

        super().delete(*args, **kwargs)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11 , unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField

    def __str__(self) -> str:
        return f"{self.phone_number} - {self.code} - {self.created}"
