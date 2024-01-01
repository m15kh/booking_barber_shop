from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# local
from .models import BarberUser, BarberProfile,CustomerProfile, CustomerUser


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
