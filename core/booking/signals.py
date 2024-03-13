from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from .models import TimeRange
from accounts.models import BarberProfile
# local
from .utils import TimeSlotgenerator


@receiver(post_save, sender=TimeRange)
def update_count(sender, instance, created, **kwargs):
    if created:

        all_timeslot = TimeSlotgenerator(
            instance.workstart.strftime("%H:%M"),
            instance.workfinish.strftime("%H:%M"),
            instance.reststart.strftime("%H:%M"),
            instance.restfinish.strftime("%H:%M"),
            instance.duration,
        )
        instance.number_timeslots = all_timeslot[1]
        instance.save()

        barber_profile = instance.barber.user.barberprofile
        # Setting the reservation_system field to True
        barber_profile.reservation_system = True
        barber_profile.save()
        print("Reservation system set to True for barber profile:", barber_profile)


@receiver(post_delete, sender=TimeRange)
def update_barber_profile_on_delete(sender, instance, **kwargs):
    remaining_time_ranges = TimeRange.objects.filter(barber=instance.barber).exists()
    if not remaining_time_ranges:
        barber_profile = instance.barber.user.barberprofile
        # Setting the reservation_system field to False
        barber_profile.reservation_system = False
        barber_profile.save()
        print("Reservation system set to False for barber profile:", barber_profile)
   