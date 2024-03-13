from django.db import models
from accounts.models import CustomerProfile, BarberProfile
# local
from .utils import Dateslotgenerator


from django.db import models
from django.core.exceptions import ValidationError
# 3rd party
from datetime import datetime


class TimeRange(models.Model):
    DAYS_OF_WEEK = (
        (0, "Saturday"),
        (1, "Sunday"),
        (2, "Monday"),
        (3, "Tuesday"),
        (4, "Wednesday"),
        (5, "Thursday"),
        (6, "Friday"),
    )

    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE)

    Days = models.IntegerField(
        choices=DAYS_OF_WEEK,
    )

    workstart = models.TimeField()
    workfinish = models.TimeField()
    reststart = models.TimeField()
    restfinish = models.TimeField()
    duration = models.IntegerField(
        choices=(
            (15, "15 minute"),
            (30, "30 minute"),
            (45, "45 minute"),
            (60, "60 minute"),
        )
    )
    number_timeslots = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (
            "barber",
            "Days",
        )  # you can't have multiple appointments with the same barber on the same date and timeslot.

    def __str__(self):
        day_name = self.get_Days_display()
        return " {} ".format(
            day_name,
        )

    def get_day_name(self):
        return dict(self.DAYS_OF_WEEK).get(self.Days, "Unknown")


    def clean(self):
            if self.workstart >= self.workfinish:
                raise ValidationError({'workstart': 'Work start time must be earlier than or equal to work finish time.'})
            
            if self.reststart > self.restfinish:
                raise ValidationError({'reststart': 'Rest start time must be earlier than or equal to rest finish time.'})
            
            # If rest start and finish times are equal, it means no rest time is needed
            if (self.reststart != self.restfinish):
                # Additional validation: check if rest time falls within the work time range
                if self.reststart and self.restfinish:
                    if self.reststart < self.workstart or self.restfinish > self.workfinish:
                        raise ValidationError('Rest time must be within the work time range.')

class Booking(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE)
    date = models.DateField(choices=Dateslotgenerator())
    time = models.TimeField()
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE,)
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "barber",
            "date",
            "time",
        )



    def __str__(self):
        return "{} {} {}. customer: {}".format(
            self.date, self.time, self.barber, self.customer
        )


class ExcludedDates(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE)

    date = models.DateField()

    class Meta:
        unique_together = (
            "date",
            "barber",
        )

    def __str__(self) -> str:
        return "{}".format(self.date, self.barber)
