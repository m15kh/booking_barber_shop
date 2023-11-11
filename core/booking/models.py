from django.db import models
from accounts.models import BarberProfile, CustomerProfile

# local
from .utils import Dateslotgenerator


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


class Booking(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE)
    date = models.DateField(choices=Dateslotgenerator())
    timeslot = models.TimeField()
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "barber",
            "date",
            "timeslot",
        )  # you can't have multiple appointments with the same barber on the same date and timeslot.

    def __str__(self):
        return "{} {} {}. customer: {}".format(
            self.date, self.timeslot, self.barber, self.customer
        )

    # @property
    # def time(self):
    #     return self.TIMESLOT_LIST[self.timeslot][1]
