from django.db import models
from django.contrib.auth import get_user_model

# local
from .utils import Dateslotgenerator

CustomUser = get_user_model()


   
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

    Days = models.IntegerField(
        choices=DAYS_OF_WEEK, unique=True
    ) 

    workstart = models.TimeField()
    workfinish = models.TimeField()
    reststart = models.TimeField()
    restfinish = models.TimeField()
    duration = models.IntegerField(choices=((15, "15 minute"), (30, "30 minute"), (45, "45 minute"), (60, "60 minute")))

    def __str__(self):
        day_name = self.get_Days_display()
        return "{} | work: {} | work: {} | rest: {} | rest: {} |  Duration:{}".format(
            day_name,
            self.workstart,
            self.workfinish,
            self.reststart,
            self.restfinish,
            self.duration,

        )
     



class Booking(models.Model):

    class Meta:
        unique_together = (
            "barber",
            "date",
            "timeslot",
        )  # you can't have multiple appointments with the same barber on the same date and timeslot.

    barber = models.ForeignKey("Barber", on_delete=models.CASCADE)
    date = models.DateTimeField(choices=Dateslotgenerator())
    timeslot = models.TimeField()
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return "{} {} {}. customer: {}".format(
            self.date, self.time, self.barber, self.customer
        )

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Barber(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.last_name, self.short_name)

    @property
    def short_name(self):
        return "{} {}.{}.".format(
            self.last_name.title(),
            self.first_name[0].upper(),
            self.middle_name[0].upper(),
        )




