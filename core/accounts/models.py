from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMERUSER = "CUSTOMERUSER", "CustomerUser"
        BARBERUSER = "BARBERUSER", "BarberUser"

    base_role = Role.ADMIN

    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(r"^\d{11}$", "Enter a valid 11-digit phone number.")
        ],
        blank=True,
        null=True,
    )
    date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


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


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customerprofile')
    image = models.ImageField(upload_to="customers/", default="customers/default.jpg")

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        # Delete associated BarberUser
        customer_user = CustomerProfile.objects.filter(id=self.user.id)
        if customer_user.exists():
            customer_user.delete()

        # Call the parent class delete method
        super().delete(*args, **kwargs)


@receiver(post_delete, sender=CustomerProfile)
def delete_user(sender, instance, **kwargs):
    # Delete associated BarberUser
    customer_user = CustomerUser.objects.filter(id=instance.user.id)
    if customer_user.exists():
        customer_user.delete()


@receiver(post_save, sender=CustomerUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMERUSER":
        CustomerProfile.objects.create(user=instance)


class BarberUSERManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BARBERUSER)


class BarberUser(User):
    base_role = User.Role.BARBERUSER
    barberuser = BarberUSERManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for barbers"


class BarberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='barberprofile')
    image = models.ImageField(upload_to="barbers/", default="barbers/default.jpg")

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        # Delete associated BarberUser
        barber_user = BarberUser.objects.filter(id=self.user.id)
        if barber_user.exists():
            barber_user.delete()

        super().delete(*args, **kwargs)


@receiver(post_save, sender=BarberUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BARBERUSER":
        BarberProfile.objects.create(user=instance)


@receiver(post_delete, sender=BarberProfile)
def delete_user(sender, instance, **kwargs):
    # Delete associated BarberUser
    barber_user = BarberUser.objects.filter(id=instance.user.id)
    if barber_user.exists():
        barber_user.delete()
