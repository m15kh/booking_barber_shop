from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        BARBER = "BARBER", "Barber"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not  self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)

class Customer(User):

    base_role = User.Role.CUSTOMER
    student = CustomerManager()
    class Meta:
        proxy = True
    def welcome(self):
        return "Only for CUSTOMERS"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11) 
    date  = models.DateField(null=True, blank=True) 



    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user=instance)




class BarberManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BARBER)


class Barber(User):
    base_role = User.Role.BARBER
    barber = BarberManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for barbers"


class BarberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='barbers/', default='barbers/default.jpg' )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Barber)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BARBER":
        BarberProfile.objects.create(user=instance)