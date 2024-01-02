from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .models import TimeRange

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
